#!./new_env/bin/python3
""" The app definition """

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.routes import app_routes
from os import environ
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.register_blueprint(app_routes)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ App contxt to teardown connection after user """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 error page """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
