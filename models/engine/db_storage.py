#!/usr/bin/python3
"""This module defines the DBStorage class for database storage."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.base_model import Base
from os import getenv
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """This class manages the database storage for the application."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance."""
        db_user = getenv("HBNB_MYSQL_USER")
        db_pwd = getenv("HBNB_MYSQL_PWD")
        db_host = getenv("HBNB_MYSQL_HOST")
        db_name = getenv("HBNB_MYSQL_DB")
        db_env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(db_user, db_pwd,
                                             db_host, db_name),
                                      pool_pre_ping=True)

        if db_env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects from the current database session."""
        obj_dict = {}
        classes = {"User": User, "State": State,
                   "City": City, "Amenity": Amenity,
                   "Place": Place, "Review": Review}

        if cls is None:
            for cls in classes.values():
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    obj_dict[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                obj_dict[key] = obj

        return obj_dict
    '''
    def all(self, cls=None):
        """This method queries on the current database session"""
        from models.base_model import BaseModel
        from models.engine.file_storage import FileStorage

        classes = {"User": User, "State": State,
                   "City": City, "Amenity": Amenity,
                   "Place": Place, "Review": Review}
        if cls is None:
            objs = []
            for c in classes.values():
                objs += self.__session.query(c).all()
        else:
            if cls in classes:
                objs = self.__session.query(classes[cls]).all()
            else:
                objs = []
        return {obj.__class__.__name__ + '.' + obj.id: obj for obj in objs}'''

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and current database session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        '''Closes the storage engine'''
        self.__session.close()
