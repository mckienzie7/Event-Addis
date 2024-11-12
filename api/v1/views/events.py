#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Catagories"""
from sqlalchemy.orm import joinedload

from models.place import Place
from models.user import User
from models.event import Events
from models.catagory import Catagory
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
import os
import re
from dateutil import parser as date_parser  # Import dateutil parser
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

    return jsonify(ev.to_dict())

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
def create_event(user_id):
    """Create events"""
    user = storage.get(User, user_id)
    if not user:
        abort(400, description="No user found")

    data = request.json
    if not data:
        abort(400, description="Missing JSON data")

    if 'place_id' not in data:
        abort(400, description="Missing place_id")
    if 'title' not in data:
        abort(400, description="Missing title")

    place = storage.get(Place, data['place_id'])
    if not place:
        abort(401, description="No place found")

    banner_data = data.get('Banner', '')
    if banner_data:
        banner_data = re.sub(r'^data:image/[^;]+;base64,', '', banner_data)
        missing_padding = len(banner_data) % 4
        if missing_padding:
            banner_data += '=' * (4 - missing_padding)

        try:
            data['Banner'] = base64.b64decode(banner_data)
        except (base64.binascii.Error, ValueError):
            abort(401, description="Invalid base64 data for Banner")

    data['user_id'] = user_id
    data['Address'] = place.address

    # Convert and validate the event date using dateutil.parser for flexibility
    event_date_str = data.get('Date')
    try:
        # Use dateutil's parser to handle multiple date formats
        event_date = date_parser.parse(event_date_str)
    except (ValueError, TypeError):
        abort(401, description="Invalid date format. Use a valid ISO format like YYYY-MM-DDTHH:MM:SS")

    current_time = datetime.now()
    data['status'] = 'Active' if event_date >= current_time else 'Cancelled'

    # Ensure 'catagories' field contains valid category instances
    if 'catagories' not in data:
        abort(400, description="Missing catagories field")

    categories = []
    for cat_id in data['catagories']:
        catagory = storage.get(Catagory, cat_id)
        if not catagory:
            abort(400, description=f"No category found with id {cat_id}")
        categories.append(catagory)

    # Remove 'catagories' key from data to avoid conflict
    del data['catagories']

    # Create event instance
    instance = Events(**data)
    instance.catagories = categories  # Set the many-to-many relationship
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)
@app_views.route('/event_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/event/event_search.yml', methods=['POST'])
def event_search():
    """
    Search for events by category_id, title, and address.
    :return: JSON response with matching events
    """
    if request.method == 'POST':
        search_params = request.json
        filters = []

        # If no parameters are provided, return all events
        if not search_params:
            matching_events = [event.to_dict() for event in storage.all(Events).values()]
            return jsonify(matching_events)

        # Handle 'category_id' search
        if 'category_id' in search_params:
            category_id = search_params['category_id']
            filters.append(lambda event: event.category and category_id == event.category.id)

        # Handle 'title' search (substring match)
        if 'title' in search_params:
            event_name = search_params['title'].lower()  # Case insensitive search
            filters.append(lambda event: event_name in event.title.lower())

        # Handle 'address' search (substring match)
        if 'address' in search_params:  # Adjusted to lowercase key 'address'
            event_address = search_params['address'].lower()  # Case insensitive search
            filters.append(lambda event: event_address in event.Address.lower())

        # Search for events with matching filters
        matching_events = [
            event.to_dict() for event in storage.all(Events).values()
            if all(f(event) for f in filters)
        ]

        if matching_events:
            return jsonify(matching_events)
        else:
            return jsonify({'error': 'No matching events found'}), 404

    else:
        return jsonify({'error': 'Method not allowed'}), 405
