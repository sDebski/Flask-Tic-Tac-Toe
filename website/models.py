from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    sessions = relationship('Session', back_populates='user')

    
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    points = db.Column(db.Integer, default=10)
    finished = db.Column(db.Boolean, default=False)
    user = relationship('User', back_populates='sessions')
    
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session1_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session2_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable = True)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True)
    result = db.Column(db.Integer, default = 0)
    
    session1 = relationship('Session', foreign_keys='session1_id')
    user1 = relationship('User', foreign_keys='user1_id')
    session1 = relationship('Session', foreign_keys='session2_id')
    user2 = relationship('User', foreign_keys='user2_id')
    