from random import random
from flask import jsonify, request
from streamScript.webAPI import app
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


@app.route('/get/location/', methods=['PUT', 'GET'])
def get_location():
    print(request.headers)
    try:
        screen_name = request.get_json().get('screen_name', False)
        context = dummy_data(screen_name)
    except:
        context = HTTP401()
    return jsonify(context)