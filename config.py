import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gym_log.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False