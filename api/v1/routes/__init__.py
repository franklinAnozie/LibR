#!./new_env/bin/python3
""" views init """
from flask import Blueprint, session


api_prefix = "/api/v1"

app_routes = Blueprint("app_routes", __name__, url_prefix=api_prefix)
frontend_routes = Blueprint("frontend_routes", __name__)

from api.v1.routes.books import *  # noqa: E402
from api.v1.routes.index import *  # noqa: E402
from api.v1.routes.root import *  # noqa: E402
from api.v1.routes.users import *  # noqa: E402
