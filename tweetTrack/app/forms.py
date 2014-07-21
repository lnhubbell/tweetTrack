from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


required = 'The {} field is required.'


class ContactForm(Form):
    name = StringField(
        'Name:',
        validators=[DataRequired(required.format('name'))]
    )
    email = StringField(
        'Email:',
        validators=[
            DataRequired(required.format('email')),
            Email('Please enter a valid email')
        ]
    )
    subject = StringField(
        'Subject:',
        validators=[DataRequired(required.format('subject'))]
    )
    message = TextAreaField(
        'Message:',
        validators=[DataRequired(required.format('body'))]
    )
    send = SubmitField('Send')


class TwitterForm(Form):
    screen_name = StringField(
        'Twitter Screen Name',
        validators=[DataRequired(required.format('screen name'))]
    )
    submit = SubmitField('Find Me!')
