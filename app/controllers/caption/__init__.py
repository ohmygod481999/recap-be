from flask import Blueprint, jsonify, request
from app.models.caption import Caption, caption_schema, captions_schema
from app.models.category import Category
from app.models.user import User
from app.models.voting import Voting
from app.models.caption_tag import CaptionTag
from app.models.tag import Tag
from app.db import db

caption_controllers = Blueprint("caption", url_prefix="/caption", import_name="caption")


@caption_controllers.route("/")
def get_index():
    return "hello caption"


@caption_controllers.route('/get-news-feed', methods=['GET'])
def get_news_feed():
    # Lấy các trường dữ liệu từ request
    user_id = request.json['user_id']
    tags_id = request.json['tag_ids']
    category_id = request.json['category_id']
    limit = request.json['limit']
    offset = request.json['offset']

    tags = []

    for tag_id in tags_id:
        tag = Tag.query.get(tag_id)
        t = {
            'id': tag.id,
            'name': tag.name
        }
        tags.append(t)

    # Truy vấn các caption theo status, category, user
    results = db.session.query(Caption.id,
                               Caption.content,
                               Caption.category_id,
                               Category.name,
                               Caption.created_at,
                               Caption.author_id,
                               User.username
                               ) \
        .filter(Caption.status == 1,
                Caption.category_id == Category.id,
                Caption.category_id == category_id,
                Caption.author_id == User.id,
                Caption.author_id == user_id,
                # CaptionTag.caption_id == Caption.id
                ) \
        .all()

    json_results = []

    for result in results:
        check = 0
        dem = 0
        tag_filters = db.session.query(CaptionTag.caption_id,
                                       CaptionTag.tag_id,
                                       Caption.id,
                                       ) \
            .filter(result.id == CaptionTag.caption_id,
                    Caption.status == 1,
                    Caption.category_id == Category.id,
                    Caption.category_id == category_id,
                    Caption.author_id == User.id,
                    Caption.author_id == user_id,
                    CaptionTag.caption_id == Caption.id
                    ).all()
        tag_list = []
        for tag_filter in tag_filters:
            tag_list.append(tag_filter.tag_id)

        if len(tag_list) == len(tags_id):
            for tag_list_id in tag_list:
                if tag_list_id in tags_id:
                    dem = dem + 1

        if dem == len(tags_id):
            check = 1

        d = {
            'id': result.id,
            'author': {
                'id': result.author_id,
                'name': result.username
            },
            'content': result.content,
            'upvote': Voting.query.filter(Voting.caption_id == result.id).count(),
            'created_at': result.created_at,
            'tags': tags,
            'category': {
                'id': result.category_id,
                'name': result.name
            }
        }
        if check == 1:
            json_results.append(d)

    json_results_limit = json_results[offset: offset + limit]

    return jsonify(json_results_limit)


@caption_controllers.route('/get-all-captions', methods=['GET'])
def get_all_captions():  # put application's code here
    all_captions = Caption.query.all()
    results = captions_schema.dump(all_captions)
    return jsonify(results)


@caption_controllers.route('/get-caption/<id>', methods=['GET'])
def get_caption(id):
    caption = Caption.query.get(id)
    return caption_schema.jsonify(caption)


@caption_controllers.route('/add-caption', methods=['POST'])
def add_caption():
    content = request.json['content']
    author_id = request.json['author_id']
    status = 0
    category_id = request.json['category_id']

    caption = Caption(content, author_id, status, category_id)
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
