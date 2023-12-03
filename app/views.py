'''Flask imports'''
from flask import render_template, redirect, url_for, request, flash, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy import and_



'''Local Imports'''
from app import app, db, admin
from app.models import db, User, Event
from app.forms import RegistrationForm, LoginForm, EventForm, EventFilterForm, EditProfileForm

class UserAdmin(ModelView):
    column_list = ('id', 'username', 'events_attending', 'created_events', 'liked_events')

class EventAdmin(ModelView):
    column_list = ('id', 'title', 'start_datetime','end_datetime', 'duration', 'location', 'description', 'attendees', 'likes')

admin.add_view(UserAdmin(User, db.session))
admin.add_view(EventAdmin(Event, db.session))

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    '''Dashboard'''
    user = current_user
    form = EventForm()

    current_datetime = datetime.utcnow()
    total_event_count = Event.query.filter(Event.start_datetime >= current_datetime).count()
    total_joined_event = Event.query.filter(and_(Event.start_datetime >= current_datetime, Event.attendees.any(id=current_user.id))).count()
    total_manage_event = Event.query.filter(Event.creator == current_user, Event.start_datetime >= current_datetime).count()
    total_past_event = Event.query.filter(Event.start_datetime < current_datetime).count()

    return render_template('home.html', form=form, user=user, total_event_count=total_event_count, total_manage_event=total_manage_event, total_joined_event=total_joined_event, total_past_event=total_past_event)

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
    '''Parse all the joined events and outputs it'''
    form = EventFilterForm()
    current_datetime = datetime.utcnow()
    my_events = Event.query.filter(and_(Event.start_datetime >= current_datetime, Event.attendees.any(id=current_user.id)))
    my_events = my_events.order_by(Event.start_datetime)

    if form.validate_on_submit():
        my_events = get_filtered_events(my_events, form.event.data, form.creator.data, form.liked.data, form.date.data)

    # Logic to fetch and display upcoming events
    return render_template('myevents.html', my_events=my_events, form=form)

@app.route('/upcoming', methods=['GET', 'POST'])
@login_required
def upcomingevents():
    '''Gets all the upcoming events and outputs it'''
    form = EventFilterForm()
    current_datetime = datetime.utcnow()
    all_events = Event.query.filter(Event.start_datetime >= current_datetime)
    # Sorts to to earliest date first
    all_events = all_events.order_by(Event.start_datetime)

    if form.validate_on_submit():
        all_events = get_filtered_events(all_events, form.event.data, form.creator.data, form.liked.data, form.date.data)

    # Logic to fetch and display event categories
    return render_template('upcomingevents.html', all_events=all_events, form=form)

@app.route('/pastevents', methods=['GET', 'POST'])
@login_required
def pastevents():
    '''Gets all the past] events and outputs it'''
    form = EventFilterForm()
    current_datetime = datetime.utcnow()
    all_events = Event.query.filter(Event.start_datetime < current_datetime)
    # Sorts to to earliest date first
    all_events = all_events.order_by(Event.start_datetime)

    if form.validate_on_submit():
        all_events = get_filtered_events(all_events, form.event.data, form.creator.data, form.liked.data, form.date.data)

    # Logic to fetch and display event categories
    return render_template('pastevents.html', all_events=all_events, form=form)


def get_filtered_events(evt, event, creator, liked, date):
    '''Filters event output based on the parameters'''
    if event:
        evt = evt.filter(Event.title.contains(event))

    if creator:
        evt = evt.filter(Event.creator.has(username=creator))

    if liked:
        evt = evt.filter(Event.likes.any(id=current_user.id))

    if date:
        evt = evt.filter(Event.start_datetime >= date)

    evt = evt.all()
    return evt

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def createevents():
    form = EventForm()

    if form.validate_on_submit():
        title = form.title.data
        start_datetime = form.start_datetime.data
        end_datetime = form.end_datetime.data
        location = form.location.data
        description = form.description.data

        # To Calculate the duration of the event
        duration = end_datetime - start_datetime
        days = duration.days
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = remainder // 60

        new_event = Event(title=title, start_datetime=start_datetime, end_datetime=end_datetime, duration=duration, location=location, description=description, creator=current_user)
        db.session.add(new_event)
        db.session.commit()

        flash('Event created successfully!', 'success')
        return redirect(url_for('manageevents'))

    return render_template('createevents.html', form=form)

@app.route('/join_event/<int:event_id>')
def join_event(event_id):
    '''function route to join events'''
    event = Event.query.get(event_id)
    if event is None:
        flash('Event not available')
        return redirect(url_for('upcomingevents'))

    if current_user in event.attendees:
        flash('Already joined this event.')
        return redirect(url_for('upcomingevents'))

    event.attendees.append(current_user)
    db.session.commit()

    flash('You have successfully joined the event!')
    return redirect(url_for('upcomingevents'))

@app.route('/leave_event/<int:event_id>')
def leave_event(event_id):
    '''function route to Leave events'''
    event = Event.query.get(event_id)

    if current_user not in event.attendees:
        flash('Already left this event.')
        return redirect(url_for('myevents'))

    event.attendees.remove(current_user)
    db.session.commit()

    flash('You have successfully left the event!')
    return redirect(url_for('myevents'))

@app.route('/like_event',  methods=['GET', 'POST'])
def like_event():
    '''function to handle ajax request to update like counts for event'''
    event_id = request.form.get('event_id')
    event = Event.query.get(event_id)

    if current_user in event.likes:
        event.likes.remove(current_user)
        db.session.commit()
        return jsonify({'success': False, 'likes': len(event.likes)})

    event.likes.append(current_user)
    db.session.commit()
    return jsonify({'success': True, 'likes': len(event.likes)})
    
@app.route('/manage_events',  methods=['GET', 'POST'])
@login_required
def manageevents():
    form = EventFilterForm()
    current_datetime = datetime.utcnow()
    my_created_events = Event.query.filter(and_(Event.creator_id == current_user.id, Event.start_datetime >= current_datetime)).all()

    return render_template('manageevents.html', my_created_events=my_created_events, form=form)

@app.route('/delete_event/<int:event_id>',  methods=['GET', 'POST'])
@login_required
def delete_event(event_id):
    '''function route to delete events'''
    event = Event.query.get_or_404(event_id)

    db.session.delete(event)
    db.session.commit()

    flash('Event deleted successfully')
    return redirect(url_for('manageevents'))

@app.route('/edit_event/<int:event_id>',  methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    '''function route to edit events'''
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)

    if form.validate_on_submit():
        event.title = form.title.data
        event.start_datetime = form.start_datetime.data
        event.end_datetime = form.end_datetime.data
        event.location = form.location.data
        event.description = form.description.data

        # To Calculate the duration of the event
        event.duration = event.end_datetime - event.start_datetime
        days = event.duration.days
        hours, remainder = divmod(event.duration.seconds, 3600)
        minutes = remainder // 60

        # Save the changes to the database
        db.session.commit()

        flash('Event updated successfully!')
        return redirect(url_for('manageevents'))

    return render_template('editevents.html', form=form, event=event)

@app.route('/profile',  methods=['GET', 'POST'])
@login_required
def profile():
    user=current_user
    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        if form.new_username.data:
            # Check if the new username is not taken
            if form.new_username.data != current_user.username and User.query.filter_by(username=form.new_username.data).first():
                flash('Username is already taken. Please choose a different one.', 'danger')
            else:
                current_user.username = form.new_username.data

        if current_user.first_name != form.first_name.data:
            current_user.first_name = form.first_name.data

        if current_user.last_name != form.last_name.data:
            current_user.last_name = form.last_name.data

        if form.email.data != current_user.email and User.query.filter_by(email=form.email.data).first():
                flash('Email is already taken. Please choose a different one.', 'danger')
        else:
            current_user.email = form.email.data

        db.session.commit()
        flash('Profile succesfully updated')
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user, form=form)

@app.route("/cookie-policy")
def cookie_policy():
    # Your cookie policy content here
    return render_template("cookie_policy.html")

@app.route('/clear_cookie')
def clear_cookie():
    # Clear the 'user' cookie
    response = make_response("Cookie has been cleared!")
    response.delete_cookie('user')
    flash("Cookie has been cleared!")
    return render_template("cookie_policy.html")