from app.db import db, ma
import datetime

# Khai báo bảng Caption
class Caption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    author_id = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.Integer)

    def __init__(self, content, author_id, status):
        self.content = content
        self.author_id = author_id
        self.status = status

class CaptionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content', 'author_id', 'date', 'status')


caption_schema = CaptionSchema()
captions_schema = CaptionSchema(many=True)