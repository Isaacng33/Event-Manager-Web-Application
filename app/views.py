'''Flask imports'''
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.exc import IntegrityError
from datetime import datetime

'''Local Imports'''
from app import app, db, admin
from app.models import db, User, Event
from app.forms import RegistrationForm, LoginForm, EventForm

class UserAdmin(ModelView):
    column_list = ('id', 'username', 'events_attending')

class EventAdmin(ModelView):
    column_list = ('id', 'title', 'date', 'location', 'attendees')

admin.add_view(UserAdmin(User, db.session))
admin.add_view(EventAdmin(Event, db.session))

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    '''Dashboard'''
    user = current_user
    event_count = user.events_attending_count()

    return render_template('home.html', user=user, event_count=event_count)

'''Code to handle login authentication'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # Log in the user
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        
        flash('Incorrect username or password. Please try again.', 'danger')

    return render_template('loginpage.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Register Page'''
    form = RegistrationForm()
  
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Checks if username is already taken
        try:
            new_user = User(username=username)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

    return render_template('registerpage.html', form=form)

@app.route('/logout')
@login_required
def logout():
    '''Make sure user is logon to be able to log out'''
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/myevents', methods=['GET', 'POST'])
@login_required
def myevents():
    # Logic to fetch and display upcoming events
    return render_template('myevents.html')

@app.route('/upcoming', methods=['GET', 'POST'])
@login_required
def upcomingevents():
    all_events = Event.query.all()
    # Logic to fetch and display event categories
    return render_template('upcomingevents.html', all_events=all_events)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def createevents():
    form = EventForm()

    if form.validate_on_submit():
        title = form.title.data
        date = form.date.data
        time = form.time.data
        location = form.location.data
        description = form.description.data

        new_event = Event(title=title, date=date, time=time, location=location, description=description, creator=current_user)
        db.session.add(new_event)
        db.session.commit()

        flash('Event created successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('createevents.html', form=form)