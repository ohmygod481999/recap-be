from app.db import db, ma
from sqlalchemy.dialects.postgresql import UUID
import uuid

import datetime


# Khai báo bảng Caption
class Caption(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.Text())
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    release_at = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    emotion = db.Column(db.Integer)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id'))

    def __init__(self, content, author_id, created_at, status, category_id, emotion, release_at):
        self.content = content
        self.status = status
        self.author_id = author_id
        self.created_at = created_at
        self.release_at = release_at
        self.category_id = category_id
        self.emotion = emotion


class CaptionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content', 'author_id', 'created_at', 'status', 'category_id', 'emotion', 'release_at')

class CaptionSchemaFireBase(ma.Schema):
  class Meta:
    fields = ('id', 'content', 'author_id', 'created_at', 'status', 'category_id', 'firebase_uid', 'tag_id', 'name', 'release_at')
caption_schema = CaptionSchema()
captions_schema = CaptionSchema(many=True)
captionfirebase_schema = CaptionSchemaFireBase()
captionfirebase_schemas = CaptionSchemaFireBase(many=True)
