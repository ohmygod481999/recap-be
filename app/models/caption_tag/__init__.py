from app.db import db, ma


# Khai báo bảng Caption_tag
class CaptionTag(db.Model):
    caption_id = db.Column(db.Integer, db.ForeignKey('caption.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    caption = db.relationship("Caption")
    tag = db.relationship("Tag")

    def __init__(self, caption_id, tag_id):
        self.caption_id = caption_id
        self.tag_id = tag_id


class CaptionTagSchema(ma.Schema):
    class Meta:
        fields = ('caption_id', 'tag_id')


caption_tag_schema = CaptionTagSchema()
caption_tags_schema = CaptionTagSchema(many=True)
