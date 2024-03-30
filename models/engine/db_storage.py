#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from models.catagory import Catagory
from models.event import Events
from models.notification import Notification
from models.place import Place
from models.user import User
from models.ticketing import Ticketing
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Catagory": Catagory, "Events" : Events, "Notification" : Notification,
           "Place": Place, "Ticketing": Ticketing, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        EA_MYSQL_USER = getenv('EA_MYSQL_USER')
        EA_MYSQL_PWD = getenv('EA_MYSQL_PWD')
        EA_MYSQL_HOST = getenv('EA_MYSQL_HOST')
        EA_MYSQL_DB = getenv('EA_MYSQL_DB')
        EA_ENV = getenv('EA_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(EA_MYSQL_USER,
                                             EA_MYSQL_PWD,
                                             EA_MYSQL_HOST,
                                             EA_MYSQL_DB))
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

    def find(self, cls, **kwargs):
        """
        Finds objects in the database based on given criteria
        """
        if cls not in classes.values():
            return None

        if not kwargs:
            return None

        filtered_objs = []
        all_objs = self.all(cls)

        for obj in all_objs.values():
            match = True
            for key, value in kwargs.items():
                if not hasattr(obj, key) or getattr(obj, key) != value:
                    match = False
                    break
            if match:
                filtered_objs.append(obj)

        return filtered_objs[0] if filtered_objs else None


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