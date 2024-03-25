
from flask_login import UserMixin
from sqlalchemy.sql import func 
from flask_sqlalchemy import SQLAlchemy
from .import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qualification = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bio_id = db.Column(db.Integer, db.ForeignKey('bio.id'))

class Bio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(100))
    fullname = db.Column(db.String(100))
    qualifications = db.relationship('Qualification')
    bio = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(150))
        email = db.Column(db.String(150), unique=True) #invalid if 2 emails are the same
        password = db.Column(db.String(150))
        notes = db.relationship('Note')
        bio = db.relationship('Bio')
        qualifications = db.relationship('Qualification')
        is_online = db.Column(db.Boolean, default = False) 



#create multiple databases , many to 1 relationship