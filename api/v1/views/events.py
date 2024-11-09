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
import base64
from datetime import datetime
@app_views.route('/event', methods=['GET'], strict_slashes=False)
@swag_from('documentation/event/all_events.yml')
def get_all_events():
    """
    Retrieves all list of Events in a system(Storage)
    """
    all_events = storage.all(Events).values()
    list_events = []
    for ev in all_events:
        # Check if the event's Date has passed, and update the status if necessary
        if ev.Date < datetime.now() and ev.status != 'Cancelled':  # Use datetime.now()
            ev.status = 'Cancelled'
            ev.save()  # Save the updated event status
        list_events.append(ev.to_dict())
    return jsonify(list_events)


@app_views.route('/event/<event_id>/', methods=['GET'], strict_slashes=False)
@swag_from('documentation/event/get_event.yml', methods=['GET'])
def get_event(event_id):
    """ Retrieves an Event based on id """
    ev = storage.get(Events, event_id)
    if not ev:
        abort(404)

    # Check if the event's Date has passed, and update the status if necessary
    if ev.Date < datetime.now() and ev.status != 'Cancelled':  # Use datetime.now()
        ev.status = 'Cancelled'
        ev.save()  # Save the updated event status


@app_views.route('/user/<user_id>/events', methods=['GET'], strict_slashes=False)
@swag_from('documentation/event/user_events.yml', methods=['GET'])
def get_user_events(user_id):
    """ Retrieves all events created by a specific user """

    user = storage.get(User, user_id)
    if not user:
        abort(404, description="User not found")

    # Retrieve all events for this user
    user_events = storage.all(Events).values()
    list_userevent = []
    for ue in user_events:
        if user_id == ue.user_id:
            list_userevent.append(ue.to_dict())

    if not list_userevent:
        return jsonify({"message": "No events found for this user"}), 404

    return jsonify(list_userevent)

@app_views.route('/<catagory_id>/events', methods=['GET'], strict_slashes=False)
@swag_from('documentation/event/catagory_events.yml', methods=['GET'])
def get_category_events(category_id):
    """Retrieves all events in a specific category more efficiently"""

    # Fetch the category by ID
    cat = storage.get(Catagory, category_id)
    if not cat:
        abort(404, description="Category not found")

    # Retrieve events for this category using joinedload to fetch related data in a single query
    events_in_category = storage.session.query(Events).options(joinedload(Events.catagories)).filter(
        Events.catagories.any(id=category_id)
    ).all()

    if not events_in_category:
        return jsonify({"message": "No events found for this category"}), 404

    return jsonify([event.to_dict() for event in events_in_category])

@app_views.route('/user/<user_id>/events', methods=['POST'], strict_slashes=False)
@swag_from('documentation/event/create_event.yml', methods=['POST'])
def create_event(user_id):
    """Create events"""
    user = storage.get(User, user_id)
    if not user:
        abort(400, description="No user")
    if 'place_id' not in request.json:
        abort(400, description="Missing place_id")

    if 'title' not in request.json:
        abort(400, description="Missing title")

    data = request.json
    place = storage.get(Place, data['place_id'])
    if not place:
        abort(400, description="No place")

    # Handle the Banner image (base64 to bytes)
    if 'Banner' in data:
        banner_data = data['Banner']
        if banner_data:
            # Remove the prefix (data:image/jpeg;base64,) if it exists
            if banner_data.startswith('data:image/jpeg;base64,'):
                banner_data = banner_data.split('base64,')[1]

            # Decode the base64 string to bytes
            data['Banner'] = base64.b64decode(banner_data)

    data['user_id'] = user_id
    data['Address'] = place.name

    # Convert event_date to datetime object using strptime
    event_date_str = data['Date']  # Ensure this is the correct string format
    try:
        event_date = datetime.strptime(event_date_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        abort(400, description="Invalid date format")

    current_time = datetime.now()

    if event_date < current_time:
        data['status'] = 'Cancelled'
    else:
        data['status'] = 'Active'

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
