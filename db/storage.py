#!./new_env/bin/python3

from dotenv import load_dotenv
from models.Model import Base, Customer
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv

load_dotenv()

class Storage(object):
    __engine = None
    __session = None

    def __init__(self):
        url_object = URL.create(
            "mysql+mysqlconnector",
            username = getenv("DB_USERNAME"),
            password = getenv("DB_PASSWORD"),
            host = getenv("DB_HOST"),
            database = getenv("DB_DATABASE"),
        )
        self.__engine = create_engine(url_object)
    
    def all(self, cls=None):
        objs = {}
        if cls is not None:
            for obj in self.__session.query(cls):
                objs[obj.id] = obj
        else:
            pass
        return objs
    
    def new(self, obj):
        self.__session.add(obj)
    
    def save(self):
        self.__session.commit()
    
    def delete(self, obj):
        self.__session.delete(obj)
        self.__session.commit()
    
    def close(self):
        self.__session.close()
    
    def reload(self):
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)
