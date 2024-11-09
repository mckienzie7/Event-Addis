#!/usr/bin/python3
""" Index """
from models.catagory import Catagory
from models.event import Events
from models.place import Place
from models.notification import Notification
from models.ticketing import Ticketing
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = [Catagory, Events, Place, Notification, Ticketing, User]
    names = ["caragory", "events", "places", "notifications", "ticketings", "users"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)
