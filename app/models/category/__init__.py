from app.db import db, ma


# Khai báo bảng Category
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())

    def __init__(self, name):
        self.content = name


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)