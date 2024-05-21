#!./new_env/bin/python3
""" The app definition """

from api.v1.routes import app_routes, frontend_routes
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, session
from flask_cors import CORS
from models import storage
from os import environ, getenv


load_dotenv()


app = Flask(__name__)
CORS(app)

app.secret_key = getenv('SECRET_KEY')
app.register_blueprint(frontend_routes)
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
    host = environ.get("LIBR_HOST", "0.0.0.0")
    port = environ.get("LIBR_PORT", 5000)
    app.run(host=host, port=port, threaded=True, debug=False)
