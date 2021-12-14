from app.models.caption import Caption, captions_schema
from app.models.caption_tag import CaptionTag
from app.models.tag import Tag
from app.db import db

from app.models.user import User
from app.models.voting import Voting
from app.models.tag import Tag
from .. import cache
from random import randint
from datetime import datetime 
import time
from operator import itemgetter, attrgetter
from ..db import db
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

@cache.cached(timeout=10, key_prefix='newfeed')
def get_newfeed(obj, info):
    try:
        #all_captions = captions_schema.dump(Caption.query.order_by(Caption.created_at.desc()).limit(100))
        query = captions_schema.dump(db.session.query(Caption).limit(10).all())
        print(query)
        payload = {
            "success": True
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload