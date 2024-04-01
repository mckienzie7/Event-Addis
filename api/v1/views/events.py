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
@app_views.route('/user/<user_id>/event', methods=['POST'],
                        strict_slashes=False)
@swag_from('documentation/event/create_event.yml', methods=['POST'])
def create_event(user_id):
        """
        Create events
        :param user_id:  users id
        :return: jsonify form of event
        """
        user = storage.get(User, user_id)

        if not user:
            abort(404)
        if not request.get_json():
            abort(400, description="Not a JSON")
        if 'title' not in request.get_json():
            abort(400, description="Missing Title")
        if 'Date' not in request.get_json():
            abort(400, description="Missing Date")

        if 'place_id' not in request.get_json():
            abort(400, description="Missing place_id")

        data = request.get_json()
        pl = storage.get(User, data['place_id'])

        if not pl:
            abort(404)

        instance = Events(**data)
        instance.user_id = user.id
        instance.save()
        return make_response(jsonify(instance.to_dict()), 201)
