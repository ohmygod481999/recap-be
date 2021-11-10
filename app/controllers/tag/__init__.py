from flask import Blueprint, jsonify, request
from app.models.tag import Tag, tag_schema, tags_schema

comment_controllers = Blueprint("tag", url_prefix="/tag", import_name="tag")

from app.db import db


@comment_controllers.route('/get-tag/<id>', methods=['GET'])
def get_tag(id):  # put application's code here
    tag = Tag.query.get(id)
    return tag_schema.jsonify(tag)

