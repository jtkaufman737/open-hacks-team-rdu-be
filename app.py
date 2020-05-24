from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from flask_pymongo import MongoClient
from User import User

import os
import ssl

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    mongo = MongoClient(os.environ['MONGO_URI'], ssl=True,ssl_cert_reqs=ssl.CERT_NONE)

    login = LoginManager(app)


    @app.route('/login', methods=['GET','POST'])
    def login():
        json = { 'username': 'jtkaufman737', 'password': 'test123' }

        if request.method == 'GET':
            if current_user.is_authenticated:
                return { 'status': 200, 'message': 'Logged in' }
            else:
                return { 'status': 401, 'message':  'Invalid Credentials' }

        if request.method == 'POST':
            user = mongo.covalert.users.find_one({ 'username': json['username'] })

            # user input plaintext, checks against hashed db version
            if user and User.check_password(user['password'], json['password']):
                return { 'status': 200, 'message': 'Logged in'}
            else:
                return { 'status': 401, 'message': 'Invalid Credentials'}

    @app.route('/signup', methods=['POST'])
    def signup():
        json = { 'username':'abc123',
                 'phone':'9195924799' ,
                 'email':'jtk.writes.code@protonmail.com',
                 'password':'abc123',
                 'textEnabled': 'true',
                 'subscriptions': [],
                 'emailEnabled': 'true'
                }

        json['notifications'] = []

        if json['textEnabled']:
            json['notifications'].append('sms')

        if json['emailEnabled']:
            json['notifications'].append('email')

        # Clean up data not used by db
        del json['textEnabled']
        del json['emailEnabled']

        # Create user instance for session
        pwd = generate_password_hash(json['password'])
        json['password'] = pwd
        u = User(username=json['username'], password=pwd)

        try:
            mongo.covalert.users.insert(json)
            return { 'status': 201, 'message': 'Signup successful'}
        except Exception as e:
            return { 'status': 500, 'message': e}

    @app.route('/logout')
    def logout():
        session.pop('username', None)

    @app.route('/subscribe')
    def subscribe():
        # can structure this to allow delete or addition
        return true

    @app.route('/location')
    def get():
        # I was thinking if it gets a query string it can filter, if not it returns the whole list
        return true

    return app

if __name__ == '__main__':
    create_app().run()
