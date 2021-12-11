from app.db import db, ma
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime


# Khai báo bảng Comment
class Comment(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption_id = db.Column(UUID(as_uuid=True), db.ForeignKey('caption.id'))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    parent_comment_id = db.Column(UUID(as_uuid=True))
    content = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, caption_id, user_id, parent_comment_id, content, created_at):
        self.caption_id = caption_id
        self.user_id = user_id
        self.parent_comment_id = parent_comment_id
        self.content = content
        self.created_at = created_at


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'caption_id', 'user_id', 'parent_comment_id', 'content', 'created_at')


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)