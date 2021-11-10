from app.db import db, ma
import datetime


# Khai báo bảng Comment
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    parent_comment_id = db.Column(db.Integer)
    content = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, caption_id, user_id, parent_comment_id, content):
        self.caption_id = caption_id
        self.user_id = user_id
        self.parent_comment_id = parent_comment_id
        self.content = content


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'caption_id', 'user_id', 'parent_comment_id', 'content', 'created_at')


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
