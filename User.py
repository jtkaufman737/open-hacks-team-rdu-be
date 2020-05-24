from flask_login import UserMixin
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def id(self):
        return self.username

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
