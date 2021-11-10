from app.db import db, ma
import datetime


# Khai báo bảng Caption
class Caption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship("Category")
    author = db.relationship("User")

    def __init__(self, content, author_id, created_at, status, category_id):
        self.content = content
        self.author_id = author_id
        self.status = status
        self.category_id = category_id


class CaptionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content', 'author_id', 'created_at', 'status', 'category_id')


caption_schema = CaptionSchema()
captions_schema = CaptionSchema(many=True)
