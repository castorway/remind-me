from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    
    # create user-to-reminders relationship
    reminders = db.relationship('Reminder', back_populates='user')


class Reminder(db.Model):
    __tablename__ = 'reminder'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    notes = db.Column(db.String(200))
    dosage = db.Column(db.String(100))
    time = db.Column(db.Time)
    timestring = db.Column(db.String(100))

    # create reminder-to-user relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="reminders")
