from datetime import date
from ariadne import convert_kwargs_to_snake_case
from app.db import db
from app.models.caption import Caption, caption_schema, captions_schema

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
