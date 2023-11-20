from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DateTimeField, TextAreaField, validators
from wtforms.validators import DataRequired, EqualTo, Length

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
    date = DateTimeField('Date', format='%d-%m-%Y', validators=
                         [DataRequired(message="Please use the correct format DD-MM-YYYY")], render_kw={"placeholder": "DD-MM-YYYY"})
    time = DateTimeField('Date Time', format='%H:%M', validators=[DataRequired(message="Please use the correct format HH:MM")],render_kw={"placeholder": "HH:MM"})
    location = StringField('Location', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
