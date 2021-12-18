from app.models.caption import Caption, captions_schema, captionfirebase_schemas
from app.models.users import Users, author_schema
from app.models.caption_tag import CaptionTag
from app.models.tag import Tag, tags_schema
from app.models.users import Users, users_schema
from app.db import db
from firebase_admin.auth import GetUsersResult, get_user
from app.db import cacheNewFeed

from .. import cache
from random import randint
from datetime import datetime
import time
from operator import itemgetter, attrgetter


def listCaptions_resolver(obj, info):
    try:
        # posts = [post.to_dict() for post in Caption.query.all()]
        print("run")
        all_captions = Caption.query.all()
        results = captions_schema.dump(all_captions)
        payload = {
            "success": True,
            "data": results
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def getCaption_resolver(obj, info, id):
    try:
        # posts = [post.to_dict() for post in Caption.query.all()]
        caption = Caption.query.get(id)
        payload = {
            "success": True,
            "data": caption
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def relatedCaptions_resolver(obj, info, id):
    try:
        # Lấy tất cả tag của caption hiện tại
        all_tags = CaptionTag.query.filter(CaptionTag.caption_id == id).all()
        # Lấy tất cả caption trừ caption hiện tại
        all_captions = Caption.query.filter(Caption.id != id).all()
        related_captions = []
        for caption in all_captions:
            dem = 0
            for tag in all_tags:
                related_query = CaptionTag.query.filter(CaptionTag.caption_id == caption.id,
                                                        CaptionTag.tag_id == tag.tag_id)\
                    .count()
                if related_query == 1:
                    dem = dem + 1
            if dem == len(all_tags):
                related_captions.append(caption)
            if len(related_captions) == 3:
                break
        results = captions_schema.dump(related_captions)
        payload = {
            "success": True,
            "data": results
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def getAuthor_resolver(obj, info, firebase_uid):
    try:
        get_author = get_user(firebase_uid)
        payload = {
            "success": True,
            "data": get_author
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def addCaption_resolver(obj, info, content, status):
    try:
        caption = Caption(content, status)
        db.session.add(caption)
        db.session.commit()
        payload = {
            "success": True,
            "data": "Success"
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@cache.cached(timeout=15, key_prefix='get_newfeed')
def get_newfeed(obj, info):
    start = time.time()
    try:
        all_captions = captionfirebase_schemas.dump(
            db.session.query(
                Caption.id,
                Caption.content,
                Caption.author_id,
                Caption.created_at,
                Caption.status,
                Caption.category_id,
                Users.firebase_uid)
            .join(Users, Caption.author_id == Users.id)
            .order_by(Caption.created_at.desc())
            .limit(10)
            .all()
        )
        for caption in all_captions:
            caption['tag'] = tags_schema.dump(db.session.query(Tag.id, Tag.name).join(
                CaptionTag, Tag.id == CaptionTag.tag_id).where(CaptionTag.caption_id == caption['id']).all())
            caption['author'] = author_schema.dump(
                get_user(caption['firebase_uid']))
        print("Time Load: " + str(time.time() - start))
        payload = {
            "success": True,
            "data": all_captions
        }
    except Exception as error:
        print(error)
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
