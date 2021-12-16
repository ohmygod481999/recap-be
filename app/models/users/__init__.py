from app.db import db, ma
from sqlalchemy.dialects.postgresql import UUID
import firebase_admin
from firebase_admin import credentials
import uuid

cred = credentials.Certificate("firebase-sdk.json")
firebase_admin.initialize_app(cred)


# Khai báo bảng Users
class Users(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firebase_uid = db.Column(db.Text())

    def __init__(self, id, firebase_uid):
        self.id = id
        self.firebase_uid = firebase_uid


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firebase_uid')


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)