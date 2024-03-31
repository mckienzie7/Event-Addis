#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Amenities"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/user', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """
    Retrieves all list of User in  a system
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/user/<user_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_amenity(user_id):
    """ Retrieves an user based on id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())



@app_views.route('/user/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes an User  Object
    """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


from flask import request, jsonify, make_response
from flasgger.utils import swag_from
from models.user import User
from api.v1.views import app_views

@app_views.route('/Registor', methods=['POST'])
@swag_from('documentation/user/create_user.yml', methods=['POST'])
def register_user():
    """
    Registers a new user
    """
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400


    existing_email = storage.getvalue(User,'email', data.get("email"))
    existing_username = storage.getvalue(User, 'username', data.get("username"))
    existing_phoneno = storage.getvalue(User,'phone_number', data.get("phone_number"))
    if existing_email:
        return jsonify({'message' : 'Email address already exists'}), 400
    if existing_username:
        return jsonify({'message' : 'Username already exists'}), 400
    if existing_phoneno:
        return jsonify({'message' : 'Phone Number address already exists'}), 400


    required_fields = ['email', 'fullname', 'username', 'password', 'phone_number']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing {field} parameter'}), 400


    # Create the user
    new_user = User(**data)

    new_user.save()

    return make_response(jsonify(new_user.to_dict()), 201)
