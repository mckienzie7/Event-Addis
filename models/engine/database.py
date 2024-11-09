#!/usr/bin/python3
"""
Contains the class DBStorage
"""
from datetime import datetime

import models
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.catagory import Catagory
from models.ticketing import Ticketing
from models.notification import Notification
from models.event import Events
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"User": User, "Events":  Events,"Place" : Place, "Catagory" : Catagory, "Ticketing" : Ticketing, "Notification" : Notification}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        EA_USER = getenv('EA_USER')
        EA_PWD = getenv('EA_PWD')
        EA_HOST = getenv('EA_HOST')
        EA_DB = getenv('EA_DB')
        EA_ENV = getenv('EA_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(EA_USER,
                                             EA_PWD,
                                             EA_HOST,
                                             EA_DB))
        if EA_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)
    def session(self):
        """Returning or Exposing self.__session"""
        return self.__session

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def Rollback(self):
        """Call Rallback"""
        self.__session.rollback()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())


        return count

    def cleanup_expired_sessions(self):
        """Remove expired sessions from the database."""
        current_time = datetime.utcnow()
        expired_users = self.__session.query(User).filter(User.session_expiration < current_time).all()

        for user in expired_users:
            # Remove session ID and expiration from the user
            user.session_id = None
            user.session_expiration = None

        self.__session.commit()