from app.db import db, ma
import datetime


# Khai báo bảng Voting
class Voting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption_id = db.Column(db.Integer, db.ForeignKey('caption.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    caption = db.relationship("Caption")
    user = db.relationship("User")
    comment = db.relationship("Comment")

    def __init__(self, caption_id, user_id, comment_id):
        self.caption_id = caption_id
        self.user_id = user_id
        self.comment_id = comment_id


class VotingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'caption_id', 'user_id', 'comment_id')


voting_schema = VotingSchema()
votings_schema = VotingSchema(many=True)
