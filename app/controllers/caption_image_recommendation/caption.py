import torch
from torch import nn
import torchvision.models as models
import torch.nn.functional as F
import numpy as np
import json
import torchvision.transforms as transforms
import skimage.transform
import argparse
from imageio import imread
from PIL import Image
import nltk
nltk.download('punkt')
import re
from nltk.tokenize import word_tokenize
import spacy
import vi_core_news_lg
import os
from scipy.stats import norm

spacy_vi = spacy.load("vi_core_news_lg")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model_path = "D:\DuAn\recap-be\caption_model\wiki.vi.model.bin"
# from gensim import models
# model = models.KeyedVectors.load_word2vec_format(model_path, binary=True)

stopwords = []
with open(os.path.join("caption_model","vietnamese-stopwords-dash.txt"), "r", encoding="utf8") as f:
  stopwords = f.read().split("\n")

def caption_image_beam_search(encoder, decoder, image_path, word_map, beam_size=3):
    """
    Reads an image and captions it with beam search.

    :param encoder: encoder model
    :param decoder: decoder model
    :param image_path: path to image
    :param word_map: word map
    :param beam_size: number of sequences to consider at each decode-step
    :return: caption, weights for visualization
    """

    k = beam_size
    vocab_size = len(word_map)

    # Read image and process
    img = imread(image_path)
    if len(img.shape) == 2:
        img = img[:, :, np.newaxis]
        img = np.concatenate([img, img, img], axis=2)
    # img = skimage.transform.resize(img, (256, 256))
    img = np.array(Image.fromarray(img).resize(size=(256, 256)))
    img = img.transpose(2, 0, 1)
    img = img / 255.
    img = torch.FloatTensor(img).to(device)
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
    transform = transforms.Compose([normalize])
    image = transform(img)  # (3, 256, 256)

    # Encode
    image = image.unsqueeze(0)  # (1, 3, 256, 256)
    encoder_out = encoder(image)  # (1, enc_image_size, enc_image_size, encoder_dim)
    enc_image_size = encoder_out.size(1)
    encoder_dim = encoder_out.size(3)

    # Flatten encoding
    encoder_out = encoder_out.view(1, -1, encoder_dim)  # (1, num_pixels, encoder_dim)
    num_pixels = encoder_out.size(1)

    # We'll treat the problem as having a batch size of k
    encoder_out = encoder_out.expand(k, num_pixels, encoder_dim)  # (k, num_pixels, encoder_dim)

    # Tensor to store top k previous words at each step; now they're just <start>
    k_prev_words = torch.LongTensor([[word_map['<start>']]] * k).to(device)  # (k, 1)

    # Tensor to store top k sequences; now they're just <start>
    seqs = k_prev_words  # (k, 1)

    # Tensor to store top k sequences' scores; now they're just 0
    top_k_scores = torch.zeros(k, 1).to(device)  # (k, 1)

    # Tensor to store top k sequences' alphas; now they're just 1s
    seqs_alpha = torch.ones(k, 1, enc_image_size, enc_image_size).to(device)  # (k, 1, enc_image_size, enc_image_size)

    # Lists to store completed sequences, their alphas and scores
    complete_seqs = list()
    complete_seqs_alpha = list()
    complete_seqs_scores = list()

    # Start decoding
    step = 1
    h, c = decoder.init_hidden_state(encoder_out)

    # s is a number less than or equal to k, because sequences are removed from this process once they hit <end>
    while True:

        embeddings = decoder.embedding(k_prev_words).squeeze(1)  # (s, embed_dim)

        awe, alpha = decoder.attention(encoder_out, h)  # (s, encoder_dim), (s, num_pixels)

        alpha = alpha.view(-1, enc_image_size, enc_image_size)  # (s, enc_image_size, enc_image_size)

        gate = decoder.sigmoid(decoder.f_beta(h))  # gating scalar, (s, encoder_dim)
        awe = gate * awe

        h, c = decoder.decode_step(torch.cat([embeddings, awe], dim=1), (h, c))  # (s, decoder_dim)

        scores = decoder.fc(h)  # (s, vocab_size)
        scores = F.log_softmax(scores, dim=1)

        # Add
        scores = top_k_scores.expand_as(scores) + scores  # (s, vocab_size)

        # For the first step, all k points will have the same scores (since same k previous words, h, c)
        if step == 1:
            top_k_scores, top_k_words = scores[0].topk(k, 0, True, True)  # (s)
        else:
            # Unroll and find top scores, and their unrolled indices
            top_k_scores, top_k_words = scores.view(-1).topk(k, 0, True, True)  # (s)

        # Convert unrolled indices to actual indices of scores
        prev_word_inds = top_k_words / vocab_size  # (s)
        next_word_inds = top_k_words % vocab_size  # (s)

        # Add new words to sequences, alphas
        seqs = torch.cat([seqs[prev_word_inds.long()], next_word_inds.unsqueeze(1)], dim=1)  # (s, step+1)
        seqs_alpha = torch.cat([seqs_alpha[prev_word_inds.long()], alpha[prev_word_inds.long()].unsqueeze(1)],
                               dim=1)  # (s, step+1, enc_image_size, enc_image_size)

        # Which sequences are incomplete (didn't reach <end>)?
        incomplete_inds = [ind for ind, next_word in enumerate(next_word_inds) if
                           next_word != word_map['<end>']]
        complete_inds = list(set(range(len(next_word_inds))) - set(incomplete_inds))

        # Set aside complete sequences
        if len(complete_inds) > 0:
            complete_seqs.extend(seqs[complete_inds].tolist())
            complete_seqs_alpha.extend(seqs_alpha[complete_inds].tolist())
            complete_seqs_scores.extend(top_k_scores[complete_inds])
        k -= len(complete_inds)  # reduce beam length accordingly

        # Proceed with incomplete sequences
        if k == 0:
            break
        seqs = seqs[incomplete_inds]
        seqs_alpha = seqs_alpha[incomplete_inds]
        h = h[prev_word_inds[incomplete_inds].long()]
        c = c[prev_word_inds[incomplete_inds].long()]
        encoder_out = encoder_out[prev_word_inds[incomplete_inds].long()]
        top_k_scores = top_k_scores[incomplete_inds].unsqueeze(1)
        k_prev_words = next_word_inds[incomplete_inds].unsqueeze(1)

        # Break if things have been going on too long
        if step > 50:
            break
        step += 1

    i = complete_seqs_scores.index(max(complete_seqs_scores))
    seq = complete_seqs[i]
    alphas = complete_seqs_alpha[i]

    return seq, alphas

class CaptionRecommendation:
  def __init__(self, captions):
    self.captions = captions
    for caption in self.captions:
      caption["vector"] = self.vectorize(caption["content"])

  def vectorize(self, doc: str):
    cleaned_doc = re.sub(f"[^\w]", " ", doc.lower())
    # tokens = word_tokenize(cleaned_doc)
    # non_stopword_tokens = [token for token in tokens if token not in stopwords]
    # sen = " ".join(non_stopword_tokens)
    sen = cleaned_doc
    # vecs = []
    # tokens = spacy_vi(sen)
    # for token in tokens:
    #   vecs.append(token.vector)

    vecs = [token.vector for token in spacy_vi(sen)]
    return np.mean(vecs, axis=0)

  def _cosine_sim(self, vecA, vecB):
    csim = np.dot(vecA, vecB)/(np.linalg.norm(vecA)*np.linalg.norm(vecB))
    if np.isnan(np.sum(csim)):
      return 0
    return csim

  # emotion: 'joy', 'sad'
  def recommend(self, query_string, emotion, number):
    emotion_index = 1 if emotion == 'joy' else 0
    match_emotion_captions = [caption for caption in self.captions if caption['emotion'] == emotion_index]

    query_string_vector = self.vectorize(query_string)
    n = norm(10, 1)
    similarities = [self._cosine_sim(query_string_vector, caption["vector"]) * (1 + n.pdf(len(word_tokenize(query_string))))  for caption in match_emotion_captions]
    # similarities = [spacy_vi(query_string).similarity(spacy_vi(caption["content"])) for caption in match_emotion_captions]
    sort_index = np.argsort(similarities)
    results = []
    for i in range(len(similarities) - 1 ,len(similarities) - 1-number,-1):
        c = {
            "point": similarities[sort_index[i]],
            "id": match_emotion_captions[sort_index[i]]["id"],
            "content": match_emotion_captions[sort_index[i]]["content"],
            "tags": match_emotion_captions[sort_index[i]]["tags"],
        }
        results.append(c)
        print(similarities[sort_index[i]]['content'], match_emotion_captions[sort_index[i]])
    return results

class EmotionSocialImageDetector:
  def __init__(self):
    self.classes = ['joy', 'sad']
    emotion_model = models.resnet50()
    num_ftrs = emotion_model.fc.in_features
    emotion_model.fc = nn.Linear(num_ftrs, len(self.classes))
    emotion_model = emotion_model.to(device)
    emotion_model.load_state_dict(torch.load(os.path.join("caption_model","emotion_model_resnet50.dat"), map_location='cpu'))
    self.model = emotion_model
    self.transform = transforms.Compose([
      transforms.Resize(255),
      transforms.CenterCrop(224),
      transforms.ToTensor(),
    ])
    self.samples = torch.load(os.path.join("caption_model","samples.pt"), map_location=torch.device('cpu'))

  def predict(self, image):
    image = self.transform(image)
    image = image.unsqueeze_(0).to(device)
    with torch.no_grad():
      images = torch.cat([image, self.samples], dim = 0)
      pred = self.model(images)
      pred = torch.argmax(pred[0])
      return pred.item()
      # return self.classes[pred.item()]