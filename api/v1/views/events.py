#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Catagories"""
from models.place import Place
from models.user import User
from models.event import Events
from models.catagory import Catagory
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
import os
from werkzeug.utils import secure_filename



@app_views.route('/event', methods=['GET'], strict_slashes=False)
@swag_from('documentation/event/all_events.yml')
def get_all_events():
    """
    Retrieves all list of Events in  a system(Storage)
    """
    all_events = storage.all(Events).values()
    list_events = []
    for ev in all_events:
        list_events.append(ev.to_dict())
    return jsonify(list_events)


@app_views.route('/event/<event_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/event/get_event.yml', methods=['GET'])
def get_event(event_id):
    """ Retrieves an Event based on id """
    ev = storage.get(Events, event_id)
    if not ev:
        abort(404)

    return jsonify(ev.to_dict())
@app_views.route('/user/<user_id>/events', methods=['POST'], strict_slashes=False)
@swag_from('documentation/event/create_event.yml', methods=['POST'])
def create_event(user_id):
    """
    Create events
    :param user_id: users id
    :return: jsonify form of event
    """
    user = storage.get(User, user_id)

    if not user:
        abort(400, description="No user")

    if 'place_id' not in request.json:
        abort(400, description="Missing place_id")

    if 'title' not in request.json:
        abort(400, description="Missing title")

    if 'Date' not in request.json:
        abort(400, description="Missing Date")

    if 'Banner' not in request.files:
        abort(400, description="Missing Banner")

    data = request.json
    place = storage.get(Place, data['place_id'])
    if not place:
        abort(400, description="No place")

    data['user_id'] = user_id

    instance = Events(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)
@app_views.route('/event_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/event/event_search.yml', methods=['POST'])
def event_search():
    """
    Search for events by name
    :return: JSON response with matching events
    """
    # Ensure request method is POST
    if request.method == 'POST':
        # Check if 'name' key is in the request JSON data
        if 'name' in request.json:
            # Retrieve the value of 'name' from the request JSON data
            event_name = request.json['name']
            # Search for events with matching names
            matching_events = [event.to_dict() for event in storage.all(Events).values() if event_name in event.name]
            # Return the matching events as JSON response
            return jsonify(matching_events)
        else:
            # If 'name' key is not present in the request JSON data, return an error response
            return jsonify({'error': 'Missing name parameter in request'}), 400
    else:
        # If request method is not POST, return an error response
        return jsonify({'error': 'Method not allowed'}), 405
