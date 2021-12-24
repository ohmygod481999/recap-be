from datetime import time
from flask import Flask, config
from dotenv import load_dotenv
from flask_caching import Cache
from flask_cors import CORS

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML

from flask import request, jsonify
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/caption_image_recommendation/*": {"origins": "*"}})
cache = Cache(app, config={'CACHE_TYPE':'SimpleCache'})

from app.graphql import query, schema
# Khai báo kết nối Database

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

app.config['UPLOAD_FOLDER'] = "file_upload"
if not os.path.isdir(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from app.controllers.caption import caption_controllers
from app.controllers.caption_image_recommendation import caption_image_recommendation_controllers
app.register_blueprint(caption_controllers)
app.register_blueprint(caption_image_recommendation_controllers)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

# db.create_all()

@app.route('/')
def get_index():
    return "hello phuong"