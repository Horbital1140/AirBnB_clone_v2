#!/usr/bin/python3
"""This module defines a class to manage database storage """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import Base


class DBStorage:
    """ Database storage class """
    __engine = None
    __session = None

    def __init__(self):
        """initialization function"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", default="localhost")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ querying all class objects """
        objects = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f"{type(obj).__name__}.{obj.id}"
                objects[key] = obj
        else:
            klasses = [State, City, User, Place, Review, Amenity]
            objects = {}

            for klas in klasses:
                objs = self.__session.query(klas).all()
                for obj in objs:
                    key = f"{type(obj).__name__}.{obj.id}"
                    objects[key] = obj

        return (objects)

    def new(self, obj):
        """ adding new object instance """
        self.__session.add(obj)

    def save(self):
        """ committing all changes and saving """
        self.__session.commit()

    def delete(self, obj=None):
        """ deleting an object instance """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ reloading database engine """
        Base.metadata.create_all(self.__engine)
        Sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Sess)
        self.__session = Session()

    def close(self):
        """updating database method"""
        self.__session.close()
        