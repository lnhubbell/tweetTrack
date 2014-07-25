from os import environ
from random import random
import json
import tweepy
import requests
from requests.exceptions import ConnectionError
from flask import render_template, request, jsonify
from flask.ext.mail import Message
from tweetTrack.app import app, mail
from tweetTrack.app.forms import TwitterForm, ContactForm
from tweetTrack.app.forms import UserResponseForm, APIRequestForm
from tweetTrack.app.models import UserResponse


@app.route('/')
@app.route('/index')
def index():
    contact_form = ContactForm()
    twitter_form = TwitterForm()
    api_request_form = APIRequestForm()
    user_response_form = UserResponseForm()
    return render_template(
        'index.html',
        contact_form=contact_form,
        twitter_form=twitter_form,
        api_request_form=api_request_form,
        user_response_form=user_response_form
    )


@app.route('/twitter/<user_name>')
def user_tweets(user_name):
    try:
        url = app.config['TRACKING_API_URL']
        data = json.dumps({'screen_name': user_name})
        headers = {
            'Content-Type': 'application/json',
            'Content-Length': len(data)
        }
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except ConnectionError:
        pass


# I know these methods look a lot alike, which means I should have made
# a request builder function but there is only so many hours in the day
@app.route('/api-request/<email>', methods=['GET', 'POST'])
def api_request(email):
    try:
        url = app.config['REQUEST_API_URL']
        data = json.dumps({'email': email})
        headers = {
            'Content-Type': 'application/json',
            'Content-Length': len(data)
        }
        response = requests.get(url, data=data, headers=headers)
        response.raise_for_status()
        return jsonify(response=response.json())
    except ConnectionError:
        return '<p>Something went wrong with you request</p>'


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    name = request.args.get('name', 'Name error')
    subject = request.args.get('subject', 'Subject Error')
    email = request.args.get('email', 'Email Error')
    full_subject = '{} - From: {} @ {}'.format(subject, name, email)
    msg = Message(
        full_subject,
        sender=email,
        recipients=['tweet.track@gmail.com']
    )
    msg.body = request.args.get('message', 'Message error')
    mail.send(msg)
    return render_template('message_sent.html', name=name)
