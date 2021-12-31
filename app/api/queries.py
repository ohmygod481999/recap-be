from app.models.caption import Caption, captions_schema, captionfirebase_schemas
from app.models.users import Users, author_schema
from app.models.voting import Voting, votings_schema
from app.models.comment import Comment, comments_schema
from app.models.caption_tag import CaptionTag
from app.models.tag import Tag, tags_schema
from app.models.users import Users, users_schema
from app.db import db
from firebase_admin.auth import GetUsersResult, get_user
from app.db import cacheNewFeed

from .. import cache
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
        # all_captions = Caption.query.filter(Caption.id != id).all()
        all_captions = db.session.query(
                Caption.id,
                Caption.content,
                Caption.author_id,
                Caption.created_at,
                Caption.status,
                Caption.category_id,
                Users.firebase_uid).join(Users, Caption.author_id == Users.id).all()
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
        results = captionfirebase_schemas.dump(related_captions)
        for caption in results:
            caption['tag'] = tags_schema.dump(db.session.query(Tag.id, Tag.name).join(
                CaptionTag, Tag.id == CaptionTag.tag_id).where(CaptionTag.caption_id == caption['id']).all())
            caption['author'] = author_schema.dump(
                get_user(caption['firebase_uid']))
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

@cache.memoize(60)
def get_newfeed(obj, info, limit, offset):
    start = time.time()
    try:
        all_captions = captionfirebase_schemas.dump(
            db.session.query(
                Caption.id,
                Caption.content,
                Caption.author_id,
                Caption.created_at,
                Caption.release_at,
                Caption.status,
                Caption.category_id,
                Users.firebase_uid)
            .join(Users, Caption.author_id == Users.id)
            .where(Caption.status == 1, Caption.release_at != None)
            .order_by(Caption.release_at.desc())
            .limit(int(limit))
            .offset(int(offset))
            .all()
        )
        for caption in all_captions:
            caption['tag'] = tags_schema.dump(db.session.query(Tag.id, Tag.name).join(
                CaptionTag, Tag.id == CaptionTag.tag_id).where(CaptionTag.caption_id == caption['id']).all())
            caption['author'] = author_schema.dump(
                get_user(caption['firebase_uid']))
            votes = votings_schema.dump(db.session.query(Voting.id).where(Voting.caption_id == caption['id']).all())
            comments = comments_schema.dump(db.session.query(Comment.id, Comment.content, Comment.created_at, Comment.user_id).where(Comment.caption_id == caption['id']).all())
            for comment in comments:
                childrenComments = comments_schema.dump(db.session.query(Comment.id, Comment.content, Comment.created_at, Comment.user_id).where(Comment.parent_comment_id == comment['id']).all())
                comment["comments"] = childrenComments
            caption['comments'] = comments
            caption['vote_number'] = len(votes)
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
