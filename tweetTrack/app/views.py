from os import environ
import json
from random import random
import tweepy
import requests
from flask import render_template, redirect, url_for, request, jsonify
from flask.ext.mail import Message
from tweetTrack.app import app, mail
from tweetTrack.app.forms import TwitterForm, ContactForm, APIRequestForm


def get_twitter_api():
    try:
        from tweetTrack.app.config.keys import TwitterKeys
    except ImportError:
        pass
    auth = tweepy.OAuthHandler(
        environ.get('CONSUMER_KEY', TwitterKeys.consumer_key),
        environ.get('CONSUMER_SECRET', TwitterKeys.consumer_secret)
    )
    auth.set_access_token(
        environ.get('ACCESS_KEY', TwitterKeys.access_key),
        environ.get('ACCESS_SECRET', TwitterKeys.access_secret)
    )
    return tweepy.API(auth)


@app.route('/')
@app.route('/index')
def index():
    contact_form = ContactForm()
    twitter_form = TwitterForm()
    api_request_form = APIRequestForm()
    return render_template(
        'index.html',
        contact_form=contact_form,
        twitter_form=twitter_form,
        api_request_form=api_request_form
        )


@app.route('/twitter/<user_name>')
def user_tweets(user_name):
    url = app.config['TRACKING_API_URL']
    data = json.dumps({'screen_name': user_name})
    headers = {
        'Content-Type': 'application/json',
        'Content-Length': len(data)
    }
    response = requests.get(url, data=data, headers=headers)
    response.raise_for_status()
    return jsonify(response=response.json())


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
