from app.db import db, ma


# Khai báo bảng Tag
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())

    def __init__(self, name):
        self.content = name


class TagSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)