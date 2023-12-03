from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DateTimeField, TextAreaField, BooleanField, DateField
from wtforms.validators import DataRequired, EqualTo, Length, Optional, Email

class RegistrationForm(FlaskForm):
    '''Form to handle new users'''
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=256)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    '''Form to handle existing users'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    '''Form to create new events'''
    title = StringField('Title', validators=[DataRequired()])
    start_datetime = DateTimeField('Start Date Time', validators=[DataRequired("Please use the correct format DD-MM-YYYY HH:MM")], format='%d-%m-%Y %H:%M', render_kw={"placeholder": "DD-MM-YYYY HH:MM"})
    end_datetime = DateTimeField('End Date Time', validators=[DataRequired("Please use the correct format DD-MM-YYYY HH:MM")], format='%d-%m-%Y %H:%M', render_kw={"placeholder": "DD-MM-YYYY HH:MM"})
    location = StringField('Location', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

class EventFilterForm(FlaskForm):
    event = StringField('Event', validators=[Optional()])
    creator = StringField('Creator', validators=[Optional()])
    liked = BooleanField('Show Liked Events', validators=[Optional()])
    date = DateField('Date', validators=[Optional()])
    submit = SubmitField('Apply Filters')

class EditProfileForm(FlaskForm):
    '''Form to handle existing users'''
    username = StringField('Current Username', render_kw={'readonly': True})
    new_username = PasswordField('New Username', validators=[Optional()], render_kw={'placeholder': "Optional: Enter a new username"})
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    submit = SubmitField('Update Profile')