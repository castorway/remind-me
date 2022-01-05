from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, default="")
    password = db.Column(db.String(100), default="")
    name = db.Column(db.String(100), default="")
    phone = db.Column(db.String(100), default="")
    discord = db.Column(db.String(100), default="")
    
    # create user-to-reminders relationship
    reminders = db.relationship('Reminder', back_populates='user')


class Reminder(db.Model):
    __tablename__ = 'reminder'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="")
    notes = db.Column(db.String(200), default="")
    dosage = db.Column(db.String(100), default="")
    time = db.Column(db.Time)
    timestring = db.Column(db.String(100), default="")
    lastnotif = db.Column(db.Date)

    # create reminder-to-user relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="reminders")
