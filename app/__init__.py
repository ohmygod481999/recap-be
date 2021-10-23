from flask import Flask
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)

# Khai báo kết nối Database

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from app.controllers.caption import caption_controllers
app.register_blueprint(caption_controllers)

# db.create_all()

@app.route('/')
def get_index():
    return "hello world"