#!/usr/bin/python3
""" Views index page """

from api.v1.routes import app_routes
from flask import jsonify
from models import storage
from models.Model import Customer
from models.Model import Admin
from models.Model import Staff
from models.Model import Books


classes = {
    "Customer": Customer,
    "Admin": Admin,
    "Staff": Staff,
    "Books": Books
}


@app_routes.route("/status", methods=["GET"])
def status():
    """ returns the status of the server """
    return jsonify({"status": "OK"})


@app_routes.route("/stats", methods=["GET"])
def stats():
    """returns the stats of the server"""
    objs_count = {}

    for key, values in classes.items():
        objs_count[key] = len(storage.all(values))

    return jsonify(objs_count)
