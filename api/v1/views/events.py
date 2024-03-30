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


@app_views.route('/catagory', methods=['GET'], strict_slashes=False)
@swag_from('documentation/catagory/all_catagories.yml')
def get_all_events():
    """
    Retrievs all events from system(storage)
    :return:
    """

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

