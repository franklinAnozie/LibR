#!./new_env/bin/python3
""" user route """

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


@app_routes.route("/user/<user_id>/", methods=["GET"], strict_slashes=False)
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


@app_routes.route("/user/<user_id>/borrowed_books/",
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


@app_routes.route("/user/<user_id>/fine/",
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
