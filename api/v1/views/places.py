#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Catagories"""
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/places', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/all_places.yml')
def get_places():

    """
   Retrieves all list of Place in  a system
   """
    all_place = storage.all(Place).values()
    list_places = []
    for pl in all_place:
        list_places.append(pl.to_dict())
    return jsonify(list_places)


@app_views.route('/place/<place_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def get_place(place_id):
    """ Retrieves an catagory based on id """
    pl = storage.get(Place, place_id)
    if not pl:
        abort(404)

    return jsonify(pl.to_dict())



@app_views.route('/place/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes an Place  Object
    """

    pl = storage.get(Place, place_id)

    if not pl:
        abort(404)

    storage.delete(pl)
    storage.save()

    return make_response(jsonify({}), 200)




@app_views.route('/place', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def create_place():

    """

    Creates a Place
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Place(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/place/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def put_place(place_id):
    """
    Updates a Place
    """
    pl = storage.get(Place, place_id)

    if not pl:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(pl, key, value)
    storage.save()
    return make_response(jsonify(pl.to_dict()), 200)



