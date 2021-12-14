from app.db import db, ma
from sqlalchemy.dialects.postgresql import UUID
import uuid


# Khai báo bảng CaptionTag
class CaptionTag(db.Model):
    caption_id = db.Column(UUID(as_uuid=True), db.ForeignKey('caption.id'), primary_key=True)
    tag_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tag.id'), primary_key=True)

    def __init__(self, name):
        self.name = name


class CaptionTagSchema(ma.Schema):
    class Meta:
        fields = ('caption_id', 'tag_id')


caption_tag_schema = CaptionTagSchema()
caption_tags_schema = CaptionTagSchema(many=True)
