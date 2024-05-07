#!./new_env/bin/python3
""" user route """

from api.v1.routes import app_routes
from flask import abort, jsonify, make_response, request
from models import storage
from models.Model import Books


classes = {
    "Books": Books
}


@app_routes.route("/books/", methods=["GET"], strict_slashes=False)
def get_books():
    """returns all the books"""
    books = []
    all_books = storage.all(Books)

    if all_books is not None:
        for value in all_books.values():
            books.append(value.__dict__)

    if len(books) > 0:
        for book in books:
            if '_sa_instance_state' in book:
                del book['_sa_instance_state']
    else:
        books = [{"Error": "No Book Found in Database"}]

    return jsonify(books)


@app_routes.route("/books/<book_id>/", methods=["GET"], strict_slashes=False)
def get_book(book_id):
    "returns a single customer"
    book = storage.get(Books, book_id)

    if book is not None:
        book = book.__dict__
        if '_sa_instance_state' in book:
            del book['_sa_instance_state']
    else:
        book = {"Error": "User Not Found"}

    return jsonify(book)


@app_routes.route("/books/<book_id>/borrowed_by/",
                  methods=["GET"], strict_slashes=False)
def get_borrowed_by(book_id):
    "returns all books borrowed by a user"
    borrowed_by = storage.get(Books, book_id).get_borrowed_by()
    users = []
    if len(borrowed_by) > 0:
        for user in borrowed_by:
            user = user.__dict__
            if '_sa_instance_state' in user:
                del user['_sa_instance_state']
                users.append(user)
    else:
        users = [{"Error": "User hasn't borrowed any books"}]

    return jsonify(users)


@app_routes.route('/books/', methods=["POST"], strict_slashes=False)
def post_book():
    """ creates a user """
    data = request.get_json(silent=True)
    show_book = {}
    if not data:
        abort(400, description="Not a JSON")

    new_book = Books()
    for key, value in data.items():
        setattr(new_book, key, value)
    new_book.new()
    for key, value in new_book.__dict__.items():
        if key == '_sa_instance_state':
            pass
        else:
            show_book[key] = value

    return make_response(jsonify(show_book), 201)
