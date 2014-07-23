from random import random
from flask import jsonify
from streamScript.webAPI import app


@app.route('/get/location/<screen_name>')
def get_location(screen_name):
    lat = random() * 39
    lng = random() * -98
    context = {
        'screen_name': screen_name,
        'location_lat': lat,
        'location_lng': lng,
    }
    return jsonify(context)