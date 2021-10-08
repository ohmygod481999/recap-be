import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# Khai báo kết nối Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/recap'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


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


@app.route('/')
@app.route('/get-all-captions', methods=['GET'])
def get_all_captions():  # put application's code here
    all_captions = Caption.query.all()
    results = captions_schema.dump(all_captions)
    return jsonify(results)


@app.route('/get-caption/<id>', methods=['GET'])
def get_caption(id):
    caption = Caption.query.get(id)
    return caption_schema.jsonify(caption)


@app.route('/add-caption', methods=['POST'])
def add_caption():
    content = request.json['content']
    author_id = request.json['author_id']
    status = 0

    caption = Caption(content, author_id, status)
    db.session.add(caption)
    db.session.commit()
    return caption_schema.jsonify(caption)


@app.route('/update-caption/<id>', methods=['PUT'])
def update_caption(id):
    caption = Caption.query.get(id)

    content = request.json['content']
    author_id = request.json['author_id']

    caption.content = content
    caption.author_id = author_id

    db.session.commit()
    return caption_schema.jsonify(caption)


@app.route('/delete-caption/<id>', methods=['DELETE'])
def delete_caption(id):
    caption = Caption.query.get(id)

    db.session.delete(caption)
    db.session.commit()
    return caption_schema.jsonify(caption)


if __name__ == '__main__':
    app.run(debug=True)
