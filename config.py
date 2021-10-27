import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'esgamoiyene'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
        .replace('postgres://', 'postgresql://') \
        or 'postgresql://postgres:admin@localhost/stockdb'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///stockdb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False