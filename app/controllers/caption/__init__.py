from flask import Blueprint, jsonify, request
from app.models.caption import Caption, caption_schema, captions_schema
from app import cache
from app.api.queries import get_newfeed
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


@caption_controllers.route('/caption-approved', methods=['POST'])
def update_caption():
    body = request.json
    data = body['event']['data']
    new = data['new'] # id, content, status
    if new['status'] == 1: # approved
        cache.delete_memoized(get_newfeed)
    '''
    {
        "event":{
            "session_variables":{
                "x-hasura-role":"admin"
            },
            "op":"UPDATE",
            "data":{
                "old":{
                    "status":0,
                    "author_id":"4c2f05b7-848b-4a51-8cce-b6aa2b6790d7",
                    "category_id":"2f3fa667-51d1-4703-b0cf-e35d21ded87b",
                    "emotion":1,
                    "content":"Cha mẹ em sinh em khéo quá, nên gương mặt em mới giống hệt con dâu của mẹ anh.",
                    "point":3,
                    "created_at":"2021-12-23T17:20:58.473175+00:00",
                    "id":"5132ced5-34bb-4984-9662-8e9abb9b5609"
                },
                "new":{
                    "status":1,
                    "author_id":"4c2f05b7-848b-4a51-8cce-b6aa2b6790d7",
                    "category_id":"2f3fa667-51d1-4703-b0cf-e35d21ded87b",
                    "emotion":1,
                    "content":"Cha mẹ em sinh em khéo quá, nên gương mặt em mới giống hệt con dâu của mẹ anh.",
                    "point":3,
                    "created_at":"2021-12-23T17:20:58.473175+00:00",
                    "id":"5132ced5-34bb-4984-9662-8e9abb9b5609"
                }
            },
            "trace_context":{
                "trace_id":"a9a5e32466b22407",
                "span_id":"4740d05590ff533d"
            }
        },
        "created_at":"2021-12-27T08:00:15.754192Z",
        "id":"ba99a429-cc84-420b-a406-c6491326eadf",
        "delivery_info":{
            "max_retries":0,
            "current_retry":0
        },
        "trigger":{
            "name":"caption_approved"
        },
        "table":{
            "schema":"public",
            "name":"caption"
        }
    }
    '''
    return "success"


@caption_controllers.route('/delete-caption/<id>', methods=['DELETE'])
def delete_caption(id):
    caption = Caption.query.get(id)

    db.session.delete(caption)
    db.session.commit()
    return caption_schema.jsonify(caption)