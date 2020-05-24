from flask_login import UserMixin
from flask_login import LoginManager
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password):
        print('Init running!')
        print(username)
        print(password)
        self.username = username
        self.password = password

    def get_id(self, id):
        return self.username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)
