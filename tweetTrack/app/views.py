from random import random
import tweepy
from flask import render_template, redirect, url_for, request, jsonify
from flask.ext.mail import Message
from tweetTrack.app import app, mail
from tweetTrack.app.config.keys import TwitterKeys
from tweetTrack.app.forms import TwitterForm, ContactForm


def get_twitter_api():
    auth = tweepy.OAuthHandler(
        TwitterKeys.consumer_key,
        TwitterKeys.consumer_secret
    )
    auth.set_access_token(
        TwitterKeys.access_key,
        TwitterKeys.access_secret
    )
    return tweepy.API(auth)


@app.route('/')
@app.route('/index')
def index():
    contact_form = ContactForm()
    twitter_form = TwitterForm()
    return render_template(
        'index.html',
        contact_form=contact_form,
        twitter_form=twitter_form
        )


@app.route('/twitter/<user_name>')
def user_tweets(user_name):
    api = get_twitter_api()
    # Will need the below twitter api call once classifier is ready
    # new_tweets = api.user_timeline(screen_name=user_name, count=200)
    lat = random() * 40
    lng = random() * -80
    context = {
        'screen_name': user_name,
        'location_lat': lat,
        'location_lng': lng,
    }
    return jsonify(context)


@app.route('/about/', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    msg = Message(
        request.args.get('subject', 'Subject Error'),
        sender=request.args.get('email', 'Email Error'),
        recipients=['tweet.track@gmail.com']
    )
    msg.body = request.args.get('message', 'Message error')
    mail.send(msg)
    name = request.args.get('name', 'Name error')
    return render_template('message_sent.html', name=name)