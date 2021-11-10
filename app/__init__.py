from flask import Flask
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)

# Khai báo kết nối Database

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khai báo các controllers
from app.controllers.caption import caption_controllers
app.register_blueprint(caption_controllers)

from app.controllers.comment import comment_controllers
app.register_blueprint(comment_controllers)

# from app.db import db
# db.create_all()

@app.route('/')
def get_index():
    return "hello world"