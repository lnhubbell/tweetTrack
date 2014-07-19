import tweepy
from flask import render_template, redirect, url_for
from flask.ext.mail import Message, Mail
from tweetTrack.app import app
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


@app.route('/tweets/<user_name>')
def user_tweets(user_name):
    api = get_twitter_api()
    new_tweets = api.user_timeline(screen_name=user_name, count=200)
    return render_template('tweets.html', tweets=new_tweets)


@app.route('/about/', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for(contact))
    return render_template('contact.html', form=form)