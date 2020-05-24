import os
import schedule
import sendgrid

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client


def create_app():
    app = Flask(__name__)
    load_dotenv()

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

    @app.route('/login')
    def login():
        pass

    @app.route('/signup')
    def signup():
        pass

    @app.route('/subscribe')
        # can structure this to allow delete or addition

    @app.route('/location')
       # I was thinking if it gets a query string it can filter, if not it returns the whole list

    return app


if __name__ == '__main__':
    create_app().run()
