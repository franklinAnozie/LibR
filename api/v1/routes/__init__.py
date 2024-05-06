#!./new_env/bin/python3
""" views init """
from flask import Blueprint


url_prefix = "/api/v1"

app_routes = Blueprint("app_routes", __name__, url_prefix=url_prefix)

from api.v1.routes.index import *  # noqa: E402
from api.v1.routes.users import *  # noqa: E402
