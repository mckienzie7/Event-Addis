#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
UPLOAD_FOLDER = '/c/Users/user/Documents/Github/Event-Addis'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
jwt = JWTManager(app)
CORS(app)

# Add a route to handle OPTIONS requests
@app.route('/api/v1/user/<user_id>/event', methods=['OPTIONS', 'POST'])
def handle_options(user_id):
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    return response

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ 404 Error """
    return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)

if __name__ == "__main__":
    """ Main Function """
    host = environ.get('EA_API_HOST', '0.0.0.0')
    port = int(environ.get('EA_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
