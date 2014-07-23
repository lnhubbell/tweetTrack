from random import random
from flask import jsonify, request
from streamScript.webAPI import app


def dummy_data(screen_name):
    lat = random() * 39
    lng = random() * -98
    context = {
        'screen_name': screen_name,
        'location_lat': lat,
        'location_lng': lng,
    }
    return context


@app.route('/get/location/<screen_name>')
def get_location(screen_name):
    req = request.get_json()
    print(req)
    context = dummy_data(screen_name)
    return jsonify(context)