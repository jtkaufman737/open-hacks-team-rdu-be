import os
import schedule
import sendgrid
import ssl

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from flask_pymongo import MongoClient
from User import User


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    load_dotenv()

    mongo = MongoClient(os.environ['MONGO_URI'], ssl=True,ssl_cert_reqs=ssl.CERT_NONE)

    login = LoginManager(app)

    def send_sms(phone):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body='this is a test',
            messaging_service_sid=os.getenv('TWILIO_SERVICE_SID'),
            to=phone
        )
        print(message)
        return message.sid

    def send_email(email):
        message = Mail(
            from_email='notifications@coronalert.app',
            to_emails=email,
            subject='CoronAlert Daily Notifications',
            html_content='this is a test'
        )
        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
        except Exception as e:
            print(e)

        return "success"

    def send_notifications():
        pass

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
        return True

    @app.route('/locations')
    def get():
        locations = []

        for loc in mongo.covalert.locations.find():
            del loc['_id']
            locations.append(loc)

        return { "status ": 200, "locations": locations }

    return app

if __name__ == '__main__':
    create_app().run()
