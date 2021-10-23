import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'esgamoiyene'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:admin@localhost/stocks'
    SQLALCHEMY_TRACK_MODIFICATIONS = False