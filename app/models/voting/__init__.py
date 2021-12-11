from app.db import db, ma
from sqlalchemy.dialects.postgresql import UUID
import uuid


# Khai báo bảng Voting
class Voting(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption_id = db.Column(UUID(as_uuid=True), db.ForeignKey('caption.id'))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    comment_id = db.Column(UUID(as_uuid=True), db.ForeignKey('comment.id'))

    def __init__(self, caption_id, user_id, comment_id):
        self.caption_id = caption_id
        self.user_id = user_id
        self.comment_id = comment_id


class VotingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'caption_id', 'user_id', 'comment_id')


voting_schema = VotingSchema()
votings_schema = VotingSchema(many=True)
