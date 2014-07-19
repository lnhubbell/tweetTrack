import tweepy
from flask import render_template
from tweetTrack.app import app
from tweetTrack.app.config.keys import TwitterKeys


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
    return render_template('index.html')


@app.route('/tweets/<user_name>')
def user_tweets(user_name):
    api = get_twitter_api()
    new_tweets = api.user_timeline(screen_name=user_name, count=200)
    return render_template('tweets.html', tweets=new_tweets)


@app.route('/about/', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/contact/')
def contact():
    render_template('contact.html')