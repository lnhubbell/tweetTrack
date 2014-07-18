import tweepy
from app import app
from flask import render_template


consumer_key = 'hWMHWIJYoJ4UIG0KNwXcC4pbg'
consumer_secret = '85E7dAk4ZkJEyNkQ0EbxYvavL7FeKUwEEJlXOs9QnXDwIcWL5c'
access_key = '249913463-xJhkkoiipEVF0xIJeZc9dys8N1qovmZGmgqiSLaV'
access_secret = 'q4CleTUfctg4BfQz6R5cRpa8EekBylIRzr63fCuargyDa'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/user/tweets/<user_name>')
def user_tweets(user_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    new_tweets = api.user_timeline(screen_name=user_name, count=200)
    return render_template('tweets.html', tweets=new_tweets)


@app.route('/user/followers/<user_name>')
def user_followers(user_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    followers = api.followers(screen_name=user_name, count=5000)
    return render_template('followers.html', followers=followers)