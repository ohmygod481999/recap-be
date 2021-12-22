from datetime import date
from random import random

from ariadne import convert_kwargs_to_snake_case
from app.db import db
from app.models.caption import Caption, caption_schema, captions_schema
from firebase_admin.auth import update_user, get_user

@convert_kwargs_to_snake_case
def add_caption_resolver(obj, info, content, status):
    try:
        caption = Caption(
            content=content, status=status
        )
        db.session.add(caption)
        db.session.commit()
        payload = {
            "success": True,
            "data": "Success"
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }
    return payload

@convert_kwargs_to_snake_case
def update_user_resolver(obj, info, uid, display_name, phone_number, photo_url):
    try:
        user_updated = update_user(uid, display_name=display_name, phone_number=phone_number, photo_url=photo_url)
        # user_updated = update_user(uid)
        payload = {
            "success": True,
            "data": user_updated
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
