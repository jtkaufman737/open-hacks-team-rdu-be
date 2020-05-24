from os import environ

SECRET_KEY = environ.get('SECRET_KEY')
MONGO_URI = environ.get('MONGO_URI')
