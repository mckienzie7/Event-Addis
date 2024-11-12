#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

# CORS setup for entire app with specific origin and credentials support
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:63342"}}, supports_credentials=True)

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.before_request
def handle_options():
    """ Handle OPTIONS preflight request """
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:63342")  # Frontend origin
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Authorization, Content-Type")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

@app.after_request
def apply_cors_headers(response):
    """ Ensure CORS headers are added to all responses """
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:63342"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    return response

@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'UniLove App Restful API',
    'uiversion': 3
}

Swagger(app)

if __name__ == "__main__":
    """ Main Function """
    host = environ.get('EA_API_HOST', '0.0.0.0')
    port = environ.get('EA_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
