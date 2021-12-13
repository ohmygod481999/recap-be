from app.models.caption import Caption, caption_schema, captions_schema
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

def keySortTime(obj):
    return time.mktime(datetime.strptime(obj['created_at'][:-6], "%Y-%m-%dT%H:%M:%S.%f").timetuple())

@cache.cached(timeout=4, key_prefix='newfeed')
def get_newfeed(obj, info):
    try:
        all_captions = captions_schema.dump(Caption.query.all())
        newest_captions = sorted(all_captions, key=keySortTime, reverse=True)[:100]
        payload = {
            "success": True,
            "data": newest_captions
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload