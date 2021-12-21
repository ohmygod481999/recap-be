from flask import Blueprint, jsonify, request
from app.models.caption import Caption, caption_schema, captions_schema
from app.controllers.caption_image_recommendation.caption import caption_image_beam_search
import torch
import json

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

caption_image_recommendation_controllers = Blueprint("caption_image_recommendation", url_prefix="/caption_image_recommendation", import_name="caption_image_recommendation")

from app.db import db

# model_path = "caption_model\my_model\dummy.pth.tar"
# word_map_path = "caption_model\my_model\WORDMAP_flickr8k_5_cap_per_img_5_min_word_freq.json"
model_path = "caption_model\BEST_checkpoint_coco_5_cap_per_img_5_min_word_freq.pth.tar"
word_map_path = "caption_model\WORDMAP_coco_5_cap_per_img_5_min_word_freq.json"

with open(word_map_path, 'r') as j:
    word_map = json.load(j)
rev_word_map = {v: k for k, v in word_map.items()}  # ix2word
beam_size = 5

checkpoint = torch.load(model_path, map_location=str(device))
decoder = checkpoint['decoder']
decoder = decoder.to(device)
decoder.eval()
encoder = checkpoint['encoder']
encoder = encoder.to(device)
encoder.eval()

# Load word map (word2ix)
with open(word_map_path, 'r') as j:
    word_map = json.load(j)
rev_word_map = {v: k for k, v in word_map.items()}  # ix2word

# Encode, decode with attention and beam search


@caption_image_recommendation_controllers.route("/")
def get_index():
    seq, alphas = caption_image_beam_search(encoder, decoder, "C:\\Users\\vuong\\OneDrive\\Pictures\\download.jfif", word_map, beam_size)
    words = [rev_word_map[ind] for ind in seq]

    return " ".join(words)