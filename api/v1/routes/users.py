#!./new_env/bin/python3
""" user route """

from api.v1.routes import app_routes
from flask import abort, jsonify, make_response, request
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


@app_routes.route("/users/", methods=["GET"], strict_slashes=False)
def get_users():
    """returns all the customers"""
    users = []
    all_customers = storage.all(Customer)

    if all_customers is not None:
        for value in all_customers.values():
            users.append(value.__dict__)

    if len(users) > 0:
        for user in users:
            if '_sa_instance_state' in user:
                del user['_sa_instance_state']
    else:
        users = [{"Error": "No User Found in Database"}]

    return jsonify(users)


@app_routes.route("/staff/", methods=["GET"], strict_slashes=False)
def get_staff_users():
    """returns all the staff"""
    staffs = []
    all_staff = storage.all(Staff)

    if all_staff is not None:
        for value in all_staff.values():
            staffs.append(value.__dict__)

    if len(staff) > 0:
        for staff in staffs:
            if '_sa_instance_state' in staff:
                del staff['_sa_instance_state']
    else:
        staffs = [{"Error": "No Staff Found in Database"}]

    return jsonify(staffs)


@app_routes.route("/users/<user_id>/", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    "returns a single customer"
    user = storage.get(Customer, user_id)

    if user is not None:
        user = user.__dict__
        if '_sa_instance_state' in user:
            del user['_sa_instance_state']
    else:
        user = {"Error": "User Not Found"}

    return jsonify(user)


@app_routes.route("/staff/<staff_id>/", methods=["GET"], strict_slashes=False)
def get_staff_user(staff_id):
    "returns a single staff"
    staff = storage.get(Staff, staff_id)

    if staff is not None:
        staff = staff.__dict__
        if '_sa_instance_state' in staff:
            del staff['_sa_instance_state']
    else:
        staff = {"Error": "Staff Not Found"}

    return jsonify(staff)


@app_routes.route("/users/<user_id>/borrowed_books/",
                  methods=["GET"], strict_slashes=False)
def get_borrowed_books(user_id):
    "returns all books borrowed by a user"
    borrowed_books = storage.get(Customer, user_id).get_borrowed()
    books = []
    if len(borrowed_books) > 0:
        for book in borrowed_books:
            book = book.__dict__
            if '_sa_instance_state' in book:
                del book['_sa_instance_state']
                books.append(book)
    else:
        books = [{"Error": "User hasn't borrowed any books"}]

    return jsonify(books)


@app_routes.route("/users/<user_id>/fine/",
                  methods=["GET"], strict_slashes=False)
def get_user_fines(user_id):
    "returns the total amount a user fine is"
    user_details = storage.get(Customer, user_id)
    fine = None
    if user_details is not None:
        user_details = user_details.__dict__
        fine = user_details["fine"]

    if fine is None or fine == 0:
        fine = ["User Owes no fine"]

    return jsonify(fine)


@app_routes.route('/users/', methods=["POST"], strict_slashes=False)
def post_user():
    """ creates a user """
    data = request.get_json(silent=True)
    show_user = {}
    if not data:
        abort(400, description="Not a JSON")

    if "first_name" not in data:
        abort(400, description="Missing First Name")

    if "last_name" not in data:
        abort(400, description="Missing Last Name")

    if "user_name" not in data:
        abort(400, description="Missing User Name")

    if "password" not in data:
        abort(400, description="Missing Pasword")

    if "email_address" not in data:
        abort(400, description="Missing Email Address")

    new_user = Customer()
    for key, value in data.items():
        setattr(new_user, key, value)
    new_user.new()
    for key, value in new_user.__dict__.items():
        if key == '_sa_instance_state':
            pass
        else:
            show_user[key] = value

    return make_response(jsonify(show_user), 201)


@app_routes.route('/staff/', methods=["POST"], strict_slashes=False)
def post_staff():
    """ creates a user """
    data = request.get_json(silent=True)
    show_staff = {}

    if not data:
        abort(400, description="Not a JSON")

    if "first_name" not in data:
        abort(400, description="Missing First Name")

    if "last_name" not in data:
        abort(400, description="Missing Last Name")

    if "user_name" not in data:
        abort(400, description="Missing User Name")

    if "password" not in data:
        abort(400, description="Missing Pasword")

    if "email_address" not in data:
        abort(400, description="Missing Email Address")

    if "role" not in data:
        abort(400, description="Missing Role")

    if data["role"] == "Staff":
        new_staff = Staff()
    elif data["role"] == "Admin":
        new_staff = Admin()
    else:
        abort(400, description="Please Check the Roles")

    for key, value in data.items():
        setattr(new_staff, key, value)
    new_staff.new()
    for key, value in new_staff.__dict__.items():
        if key == '_sa_instance_state':
            pass
        else:
            show_staff[key] = value

    return make_response(jsonify(show_staff), 201)


@app_routes.route("/users/<user_id>/borrow_book/",
                  methods=["PUT"], strict_slashes=False)
def put_borrow_book(user_id):
    "borrows a book"
    user = storage.get(Customer, user_id)
    data = request.get_json(silent=True)
    list_of_borrowed_books = []

    if not data:
        abort(400, description="Not a JSON")

    if "book_id" not in data:
        abort(400, description="Missing Book ID")

    borrow_status = user.borrow_book(data["book_id"])

    if borrow_status:
        borrowed_books = user.get_borrowed()
        for book in borrowed_books:
            if "_sa_instance_state" in book.__dict__:
                del book.__dict__["_sa_instance_state"]
                list_of_borrowed_books.append(book.__dict__)

    return make_response(jsonify(list_of_borrowed_books))


@app_routes.route("/users/<user_id>/pay_fine/",
                  methods=["PUT"], strict_slashes=False)
def put_pay_fines(user_id):
    "pays a fine"
    user = storage.get(Customer, user_id)
    data = request.get_json(silent=True)
    fine = None

    if "fine" not in data:
        abort(400, description="Missing payment value")

    if user is not None:
        fine = user.__dict__["fine"]

    if fine is None or fine == 0:
        fine = ["User Owes no fine"]
    else:
        fine = user.pay_fine(int(data["fine"]))

    return jsonify(fine)
