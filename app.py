from flask import Flask, request, jsonify

def create_app():
    app = Flask(__name__)

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


if __name__ == '__main__':
    create_app().run()
