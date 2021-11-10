from app.db import db, ma
import datetime


# Khai báo bảng User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
