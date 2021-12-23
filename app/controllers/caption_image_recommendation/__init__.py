from flask import Blueprint, jsonify, request, flash
from app import app
from app.models.caption import Caption, caption_schema, captions_schema
from app.models.tag import Tag, tags_schema
from app.models.caption_tag import CaptionTag
from app.controllers.caption_image_recommendation.caption import caption_image_beam_search, CaptionRecommendation
from app.controllers.caption_image_recommendation.translate import translate
from werkzeug.utils import secure_filename
import os
import torch
import json
from app.models.caption import Caption, caption_schema, captions_schema

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
query_captions = Caption.query.all()
query_captions = db.session.query(
        Caption.id,
        Caption.content).all()
captions = captions_schema.dump(query_captions)
for caption in captions:
    caption['tags'] = tags_schema.dump(db.session.query(Tag.id, Tag.name).join(
        CaptionTag, Tag.id == CaptionTag.tag_id).where(CaptionTag.caption_id == caption['id']).all())
caption_decommendation = CaptionRecommendation(captions)

@caption_image_recommendation_controllers.route("/")
def get_index():
    seq, alphas = caption_image_beam_search(encoder, decoder, "C:\\Users\\vuong\\OneDrive\\Pictures\\download.jfif", word_map, beam_size)
    words = [rev_word_map[ind] for ind in seq]

    return " ".join(words)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@caption_image_recommendation_controllers.route("/recommend", methods=["POST"])
def post_file():
    response = {
        "data": None,
        "error": None,
        "is_success": False
    }

    if 'file' not in request.files:
        response["error"] = "no file found"
        return jsonify(response)

    file = request.files['file']
    if request.form['num_cap']:
        num_cap = int(request.form['num_cap'])
    else:
        num_cap = 5

    if file.filename == '':
        response["error"] = "No selected file"
        return jsonify(response)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        seq, alphas = caption_image_beam_search(encoder, decoder, filepath, word_map, beam_size)
        os.remove(filepath)
        words = [rev_word_map[ind] for ind in seq[1:len(seq)-1]]

        caption = " ".join(words)
        translated_caption = translate(caption)

        recommend_captions = caption_decommendation.recommend(translated_caption, num_cap)
        

        response["is_success"] = True
        response["data"] = {
            "describe_image" : translated_caption,
            "captions": recommend_captions
        }

        return jsonify(response)

    response["error"] = "File is not allowed"
    return jsonify(response)