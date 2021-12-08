from flask import Blueprint, jsonify, request
from app.models.caption import Caption, caption_schema, captions_schema

caption_controllers = Blueprint("caption", url_prefix="/caption", import_name="caption")

from app.db import db

@caption_controllers.route("/")
def get_index():
    return "hello caption"


@caption_controllers.route('/get-all', methods=['GET'])
def get_all_captions():  # put application's code here
    all_captions = Caption.query.all()
    results = captions_schema.dump(all_captions)
    return jsonify(results)


@caption_controllers.route('/get-caption/<id>', methods=['GET'])
def get_caption(id):
    caption = Caption.query.get(id)
    return caption_schema.jsonify(caption)


@caption_controllers.route('/add', methods=['POST'])
def add_caption():
    content = request.json['content']
    status = 0

    caption = Caption(content, status)
    db.session.add(caption)
    db.session.commit()
    return caption_schema.jsonify(caption)


@caption_controllers.route('/update-caption/<id>', methods=['PUT'])
def update_caption(id):
    caption = Caption.query.get(id)

    content = request.json['content']
    author_id = request.json['author_id']

    caption.content = content
    caption.author_id = author_id

    db.session.commit()
    return caption_schema.jsonify(caption)


@caption_controllers.route('/delete-caption/<id>', methods=['DELETE'])
def delete_caption(id):
    caption = Caption.query.get(id)

    db.session.delete(caption)
    db.session.commit()
    return caption_schema.jsonify(caption)