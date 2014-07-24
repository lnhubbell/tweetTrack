from re import match
from random import random
from flask import jsonify, request, url_for
from flask.ext.mail import Message
from streamScript.webAPI import app, mail, db
from streamScript.webAPI.auth.models import APIKey
from streamScript.webAPI.auth.exceptions import HTTP401


def dummy_data(screen_name):
    lat = random() * 49
    lng = random() * -122
    context = {
        'screen_name': screen_name,
        'location_lat': lat,
        'location_lng': lng,
    }
    return context


@app.route('/get/location/', methods=['GET'])
def get_location():
    try:
        screen_name = request.get_json().get('screen_name', False)
        key = request.get_json().get('api_key', False)
        context = dummy_data(screen_name, key)
    except:
        context = HTTP401()
    return jsonify(context)


@app.route('/get/key', methods=['GET'])
def get_key():
    try:
        email = request.get_json().get('email', False)
        if match('^\S+@\S+[\.][0-9a-z]+$', email):
            key = APIKey()
            db.session.add(key)
            db.session.commit()
            message = Message(
                'Activate Your Key',
                sender='tweet.track@gmail.com',
                recipients=[email]
            )
            message.body = """Your tweetTrack API key is  {}.
                Please visit <a href={}>this link</a> to activate it:
                """.format(key.key, url_for('activate_key', _external=True))
            mail.send(message)
    except:
        pass


@app.route('/activate/<key>')
def activate_key(key):
    try:
        check_key = APIKey.query.filter(APIKey.key == key).one()
        check_key.activate()
        return '<h1>Your key is now active.</h1>'
    except NoResultFound:
        return '<h1>This is not a valid key</h1>'