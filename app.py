import os
import requests
import schedule
import sendgrid
import ssl
import us

from dotenv import load_dotenv
from flask import Flask, request, jsonify, session
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from flask_pymongo import MongoClient
from User import User

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config.from_pyfile('settings.py')

    mongo = MongoClient(os.environ['MONGO_URI'], ssl=True,ssl_cert_reqs=ssl.CERT_NONE)

    login = LoginManager(app)

    def send_sms(phone, subscriptions):
        try:
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            client = Client(account_sid, auth_token)
            msg_body = f'Hello! Here is your daily COVID tracking digest: \n\n'
            for sub in subscriptions:
                sub_data = get_current_single_state_data(sub)[0]
                # build subscription data
                msg_body += f"State: {sub_data['state_name']}\n"
                msg_body += f"Positive Tests: {sub_data['positive_tests']}\n"
                msg_body += f"Recovered: {sub_data['recovered']}\n"
                msg_body += f"Total Tested: {sub_data['total_tested']}\n"
                msg_body += f"Deaths: {sub_data['deaths']}\n\n"

            msg_body += "As always from your friends at CoronAlert, stay safe and we'll have more news soon."
            message = client.messages.create(
                body=msg_body,
                messaging_service_sid=os.getenv('TWILIO_SERVICE_SID'),
                to=phone
            )

            return message.sid
        except Exception as e:
            print(e)
            return { 'status_code' : 500 }

    def send_email(email, subscriptions):
        msg_body = f'Hello! Here is your daily COVID tracking digest: <br/><br/>'
        for sub in subscriptions:
            sub_data = get_current_single_state_data(sub)[0]
            # build subscription data
            msg_body += f"State: {sub_data['state_name']}<br/>"
            msg_body += f"Positive Tests: {sub_data['positive_tests']}<br/>"
            msg_body += f"Recovered: {sub_data['recovered']}<br/>"
            msg_body += f"Total Tested: {sub_data['total_tested']}<br/>"
            msg_body += f"Deaths: {sub_data['deaths']}<br/><br/>"

        msg_body += "As always from your friends at CoronAlert, stay safe and we'll have more news soon."
        message = Mail(
            from_email='notifications@ronalert.com',
            to_emails=email,
            subject='CoronAlert Daily Notifications',
            html_content=msg_body
        )
        try:
            sg = SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
        except Exception as e:
            print(e)

        response = sg.client.mail.send.post(request_body=message.get())

        return dict(
            status=response.status_code,
            body=response.body,
            headers=response.headers
        )

    def send_notifications():
        pass

    @app.route('/digest', methods=['GET']) # This would be the backdoor manual way to trigger alerts, not sure how Rick was going to do it
    def digest():
        try:
            for usr in mongo.covalert.users.find({'notifications': 'sms'}):
                if len(usr['subscriptions']):
                    send_sms(usr['phone'], usr['subscriptions'])

            for usr in mongo.covalert.users.find({'notifications': 'email'}):
                if len(usr['subscriptions']):
                    send_email(usr['email'], usr['subscriptions'])

            response = { 'status_code': 200 }
            return response
        except Exception as e:
            print(e)
            return e

    @login.user_loader # I thought this was redundant and I'd be able to get rid of it, apparently not
    def load_user(user):
        usr = mongo.covalert.users.find_one({ 'username': user })
        return usr

    @app.route('/current/<state>')
    def get_current_single_state_data(state):
        status_code = 400
        response = 'Bad request'
        if state is None:
            response = dict(message='Please specify a state and try again')
            status_code = 404
            return response, status_code
        state_response = requests.get(f'https://covidtracking.com/api/v1/states/{state}/current.json')
        if state_response.status_code == 404:
            return dict(message='State not found, please ensure you have specified a valid state code'), 404
        state_data = state_response.json()
        response = dict(state_code=state_data['state'],
                        state_name=us.states.lookup(state).name,
                        positive_tests=state_data['positive'],
                        total_tested=state_data['totalTestResults'],
                        recovered=state_data['recovered'],
                        deaths=state_data['death'])
        return response, status_code

    @app.route('/current/states')
    def get_current_all_states_data():
        status_code = 400
        response = 'Bad request'
        try:
            states_response = requests.get('https://covidtracking.com/api/v1/states/current.json')
            states_data = states_response.json()
            state_codes = [state.abbr for state in us.states.STATES]
            state_generator = (state for state in states_data if state['state'] in state_codes)
            state_list = list()
            for state in state_generator:
                state_list.append(dict(
                    state_code=state['state'],
                    state_name=us.states.lookup(state['state']).name,
                    positive_tests=state['positive'],
                    total_tested=state['totalTestResults'],
                    recovered=state['recovered'],
                    deaths=state['death']
                ))
            response = jsonify(state_list)
            status_code = 200
        except Exception as e:
            print(str(e))
            return {'message': str(e)}, 500
        return response, status_code

    @app.route('/current/us')
    def get_current_us_data():
        status_code = 400
        response = 'Bad request'
        try:
            us_response = requests.get('https://covidtracking.com/api/v1/us/current.json')
            us_data = us_response.json()[0]  # accessing [0] as tracking API returns US data only as single-item array
            response = dict(
                        positive_tests=us_data['positive'],
                        total_tested=us_data['totalTestResults'],
                        recovered=us_data['recovered'],
                        deaths=us_data['death'])
            status_code = 200
        except Exception as e:
            print(str(e))
            return {'message': str(e)}, 500
        return response, status_code

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'GET':
            if current_user.is_authenticated:
                response=dict(message='Logged in')
                status_code=200
                return response, status_code
            else:
                response=dict('Invalid Credentials')
                status_code=401
                return response, status_code
        else:
            try:
                user = mongo.covalert.users.find_one({ 'username': request.json['username'] })

                # user input plaintext, checks against hashed db version
                if user and User.check_password(user['password'], request.json['password']):
                    load_user(request.json['username'])
                    session['user'] = { 'username': request.json['username'] }
                    response = dict(message='Logged in')
                    status_code=200
                    return response, status_code
                else:
                    response = dict(message='Invalid Credentials')
                    status_code=401
                    return response, status_code
            except Exception as e:
                print(e)

    @app.route('/signup', methods=['POST'])
    def signup():
        try:
            request.json['notifications'] = []

            if request.json['textEnabled']: request.json['notifications'].append('sms')
            if request.json['emailEnabled']: request.json['notifications'].append('email')

            # Clean up data not used by db
            del request.json['textEnabled']
            del request.json['emailEnabled']

            # Create user instance for session
            pwd = generate_password_hash(request.json['password'])
            request.json['password'] = pwd
            User(username=request.json['username'], password=pwd)

            mongo.covalert.users.insert(request.json)
            response = dict(message='Signup successful')
            status_code=201
            return response, status_code
        except Exception as e:
            print(e)
            response = dict(message=f'Internal server error: {e}')
            status_code=500
            return response, status_code

    @app.route('/logout', methods=['POST'])
    def logout():
        logout_user()
        del session['user']
        response = dict(message='OK')
        status_code=200
        return response, status_code

    @app.route('/subscribe/<identifier>', methods=['POST','PATCH'])
    def process_subscriptions(identifier):
        if identifier == 'locations':
            mongo.covalert.users.update(
              { 'username' : session['user']['username'] },
              { '$set': { 'subscriptions': request.json['codes'] }}
            )

            response = dict(message='Update successful')
            status_code=204
            return response, status_code
        else:
            request.notifications = []

            if request.json['textEnabled']: request.notifications.append('sms')
            if request.json['emailEnabled']: request.notifications.append('email')

            mongo.covalert.users.update(
              { 'username': session['user']['username'] },
              { '$set': { 'notifications': request.notifications }}
            )

            response = dict(message='Update successful')
            status_code=204
            return response, status_code

    @app.route('/locations')
    def location():
        return dict(locations=[dict(code=state.abbr, name=state.name) for state in us.states.STATES], status=200), 200

    @app.route('/user', methods=['GET'])
    def user():
        try:
            user = mongo.covalert.users.find_one({ 'username': session['user']['username']})
            del user['_id']
            response = { 'message': 'OK', 'data': user }
            status_code = 200
            return response, status_code
        except Exception:
            response = dict(message='Error retrieving user. Please check that you are logged in')
            status_code = 401
            return response, status_code

    @app.route('/user/subscriptions/current', methods=['GET'])
    def user_subscription_current_data():
        try:
            user = mongo.covalert.users.find_one({ 'username': session['user']['username'] })
            subs = user['subscriptions']
            sub_data = [get_current_single_state_data(sub)[0] for sub in subs]
            response = jsonify(sub_data)
            return response
        except Exception as e:
            status_code = 500
            response = { 'message': e }
            return response, status_code

    return app


if __name__ == '__main__':
    create_app().run()
