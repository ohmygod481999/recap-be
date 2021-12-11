from datetime import time
from flask import Flask
from dotenv import load_dotenv

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML

from flask import request, jsonify
import redis
import time
import os

load_dotenv()

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

from app.graphql import query, schema
# Khai báo kết nối Database

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from app.controllers.caption import caption_controllers
app.register_blueprint(caption_controllers)

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

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc 
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def get_index():
    count = get_hit_count()
    return "hello world , this website has been seen {} times.\n".format(count)