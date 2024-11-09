#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Catagories"""
from sqlalchemy.orm import joinedload

from models.catagory import Catagory
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models.event import Events

@app_views.route('/catagory', methods=['GET'], strict_slashes=False)
@swag_from('documentation/catagory/all_catagories.yml')
def get_catagories():
    """
    Retrieves all list of Catagory in  a system
    """
    all_catagory = storage.all(Catagory).values()
    list_catagories = []
    for cata in all_catagory:
        list_catagories.append(cata.to_dict())
    return jsonify(list_catagories)


@app_views.route('/catagory/<catagory_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_catagory(catagory_id):
    """ Retrieves an catagory based on id """
    cata = storage.get(Catagory, catagory_id)
    if not cata:
        abort(404)

    return jsonify(cata.to_dict())

@app_views.route('/event/<event_id>/categories', methods=['GET'], strict_slashes=False)
def get_event_categories(event_id):
    """Retrieves all categories associated with a specific event"""

    # Fetch the event by ID
    event = storage.get(Events, event_id)
    if not event:
        abort(404, description="Event not found")

    # Retrieve categories associated with this event using joinedload
    event_with_categories = storage.session.query(Events).options(
        joinedload(Events.catagories)
    ).filter_by(id=event_id).first()

    # Extract categories and convert them to dict
    categories = [cat.to_dict() for cat in event_with_categories.catagories]

    if not categories:
        return jsonify({"message": "No categories found for this event"}), 404

    return jsonify(categories)
@app_views.route('/catagory/<catagory_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/catagory/delete_catagory.yml', methods=['DELETE'])
def delete_catagory(catagory_id):
    """
    Deletes an Catagory  Object
    """

    cata = storage.get(Catagory, catagory_id)

    if not cata:
        abort(404)

    storage.delete(cata)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/catagory', methods=['POST'], strict_slashes=False)
@swag_from('documentation/catagory/post_catagory.yml', methods=['POST'])
def post_catagory():
    """
    Creates a Catagory
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Catagory(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/catagory/<catagory_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/catagory/put_catagory.yml', methods=['PUT'])
def put_catagory(catagory_id):
    """
    Updates a Catgory
    """
    cata = storage.get(Catagory, catagory_id)

    if not cata:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(cata, key, value)
    storage.save()
    return make_response(jsonify(cata.to_dict()), 200)






