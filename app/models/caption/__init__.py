from app.db import db, ma
from sqlalchemy.dialects.postgresql import UUID
import uuid

import datetime

# Khai báo bảng Caption
class Caption(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.Text())
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.Integer)

    def __init__(self, content, status, author_id, created_at):
        self.content = content
        self.status = status
        self.author_id = author_id
        self.created_at = created_at

class CaptionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content', 'author_id', 'created_at', 'status')


caption_schema = CaptionSchema()
captions_schema = CaptionSchema(many=True)