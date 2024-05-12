import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DUMMY = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False