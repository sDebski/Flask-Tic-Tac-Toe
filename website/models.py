from . import db
from flask_login import UserMixin
from sqllachemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Columng(db.String(150))
    
class Session(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), defualt=func.now())