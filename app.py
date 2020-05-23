import os
import schedule
import sendgrid

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def create_app():
    app = Flask(__name__)
    load_dotenv()

    @app.route('/login')
    def login():

    @app.route('/signup')
    def signup():
        # new users

    @app.route('/subscribe')
        # can structure this to allow delete or addition

    @app.route('/location')
       # I was thinking if it gets a query string it can filter, if not it returns the whole list

    return app

def send_notifications():
    pass

def send_sms(phone):
    pass

def send_email(email, subscriptions):
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
        print(e.message)

if __name__ == '__main__':
    create_app().run()
