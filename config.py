import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'catch-me-if-you-can'
