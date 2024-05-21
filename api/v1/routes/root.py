#!./new_env/bin/python3
""" Views index page """

from api.v1.routes import frontend_routes
from flask import jsonify, render_template, session
from flask import request, redirect, url_for
from models import storage
from models.Model import Customer
import requests
from uuid import uuid4


@frontend_routes.route("/", methods=["GET"], strict_slashes=False)
def home():
    authenticated = 'user_id' in session
    if authenticated:
        return render_template('home.html', authenticated=authenticated)
    else:
        return render_template('login.html')


@frontend_routes.route('/login')
def login():
    if 'user_id' in session:
        # User is already authenticated, redirect to home page
        return redirect(url_for('frontend_routes.home'))
    return render_template('login.html')


@frontend_routes.route('/login-post', methods=['POST'])
def login_post():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # Query the database to retrieve the user with the specified username
    response = requests.get('http://127.0.0.1:5000/api/v1/users')
    if response.status_code == 200:
        users = response.json()
        # Find the user with the specified username
        user = None
        for single_user in users:
            if single_user.get('user_name') == username:
                user = single_user
        if user:
            if user.get('password') == password:
                # Authentication successful
                session['user_id'] = user.get('id')
                return jsonify({'message': 'Authentication successful'}), 200
            else:
                # Invalid password
                return jsonify({'error': 'Invalid password'}), 401
        else:
            # User not found
            return jsonify({'error': 'User not found'}), 404
    else:
        # Failed to retrieve user data from the API
        return jsonify({'error': 'Failed to retrieve user data'}), 500
    return jsonify({'message': 'Login successful'}), 200


@frontend_routes.route('/logout', methods=["GET"], strict_slashes=False)
def logout():
    # Clear user session to log out
    session.pop('user_id', None)
    return redirect(url_for('frontend_routes.home'))


@frontend_routes.route('/signup')
def signup():
    return render_template('signup.html')


@frontend_routes.route('/signup', methods=['POST'])
def signup_post():
    # Extract form data from the request
    data = request.json

    id = str(uuid4())
    # Extract data fields from JSON
    first_name = data.get('first')
    last_name = data.get('last')
    email_address = data.get('email')
    user_name = data.get('username')
    password = data.get('password')

    # Create a new Customer object
    new_customer = Customer(
        id=id,
        first_name=first_name,
        last_name=last_name,
        email_address=email_address,
        user_name=user_name,
        password=password,
        role='customer'
    )

    # Add the new customer to the database session
    storage.new(new_customer)

    # Commit the session to save changes to the database
    storage.save()

    # Redirect the user to the login page
    return redirect(url_for('frontend_routes.login'))


@frontend_routes.route('/about')
def about():
    return render_template('about.html')


@frontend_routes.route('/get_user_id')
def get_user_id():
    if 'user_id' in session:
        return jsonify({'user_id': session['user_id']})
    else:
        return jsonify({'user_id': None})
