from app.db import db, ma
from sqlalchemy.dialects.postgresql import UUID
import uuid


# Khai báo bảng User
class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.Text())
    username = db.Column(db.Text())
    password = db.Column(db.Text())

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'username', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
