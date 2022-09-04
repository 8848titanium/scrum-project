import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'catch-me-if-you-can'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:Lfy2335191364!@localhost/happylearning'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
