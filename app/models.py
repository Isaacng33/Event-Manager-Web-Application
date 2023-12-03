'''db import'''
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Interval

attendance = db.Table(
    'attendance',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

likes = db.Table(
    'likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Additional Fields for Basic Information (Optional Input)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)

    # Relationship to events the user is attending
    events_attending = db.relationship('Event', secondary=attendance, back_populates='attendees')
    created_events = db.relationship('Event', back_populates='creator')

    # Relationship to events the user liked
    liked_events = db.relationship('Event', secondary=likes, back_populates='likes')

    def set_password(self, password):
        """Set the user's password in hashed format."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check if the provided password matches the user's stored hashed password."""
        return check_password_hash(self.password, password)

    def events_attending_count(self):
        '''Returns the amount of the current user event count'''
        return len(self.events_attending)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    duration = db.Column(Interval, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

    # Relationship to attendees through the attendance table
    attendees = db.relationship('User', secondary=attendance, back_populates='events_attending')
    # Relationship to users who liked the event
    likes = db.relationship('User', secondary=likes, back_populates='liked_events')

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', back_populates='created_events')
