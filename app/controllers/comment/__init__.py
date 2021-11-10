from flask import Blueprint, jsonify, request
from app.models.comment import Comment, comment_schema, comments_schema

comment_controllers = Blueprint("comment", url_prefix="/comment", import_name="comment")

from app.db import db


@comment_controllers.route('/get-all-comments/<caption_id>', methods=['GET'])
def get_all_comment_of_caption(caption_id):  # put application's code here
    all_comments_of_caption = Comment.query.filter(Comment.caption_id == caption_id)
    results = comments_schema.dump(all_comments_of_caption)
    return jsonify(results)

