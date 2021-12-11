from app.db import db, ma
from sqlalchemy.dialects.postgresql import UUID
import uuid


# Khai báo bảng Tag
class Tag(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text())

    def __init__(self, name):
        self.name = name


class TagSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
