#!./new_env/bin/python3

from datetime import datetime
from sqlalchemy import Column, DATETIME, String, Integer
from sqlalchemy.orm import declarative_base
from uuid import uuid4
import  models

Base = declarative_base()

class Model(object):
    def __init__(self, **kwargs):
        if kwargs and len(kwargs) != 0:
            ##tf = "%Y-%m-%dT%H:%M:%S.%f"
            ##kwargs["updated_at"] = datetime.strptime(kwargs["updated_at"], tf)
            ##kwargs["created_at"] = datetime.strptime(kwargs["created_at"], tf)
            for key in kwargs:
                if key != "__class__":
                    setattr(self, key, kwargs[key])
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()


class Users(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def get_full_name(self):
       return f"{self.first_name} {self.last_name}"
    
    def get_user_name(self):
       return f"{self.user_name}"
    
    def change_password(self, new_password):
        self.password = new_password
        return f"{self.password}"

class Customer(Users, Base):

    __tablename__ = "customers"
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'latin1'}

    id = Column(String(256), primary_key=True)
    created_at = Column(DATETIME, default=datetime.now, nullable=False)
    updated_at = Column(DATETIME, default=datetime.now, nullable=False)
    first_name = Column(String(256))
    last_name = Column(String(256))
    email_address = Column(String(256))
    user_name = Column(String(256))
    password = Column(String(256))
    fine = Column(Integer)
    borrowed_books = Column(String(256))

    __limit = 3
    __borrowed_book = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def save(self):
        models.storage.new(self)
        models.storage.save()
    
    def get_borrowed(self):
        return len(self.__borrowed_book)
    
    def borrow_book(self, new_book):
        if len(self.__borrowed_book) <= self.__limit:
            self.__borrowed_book[new_book["id"]] = new_book
            return True
        else:
            return False
    
    def return_book(self, ret_book):
        for key, value in self.__borrowed_book.items():
            if key == ret_book["id"]:
                del(self.__borrowed_book[ret_book["id"]])
                return True


class Admin(Users):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def add_user(self, user_data):
        if user_data.role == "Admin":
            Admin(**user_data)
        elif user_data.role == "Staff":
            Staff(**user_data)
        else:
            Customer(**user_data)
    
    #def delete_user(self, user_id)
    #def manage_books(self, **kwargs)
        ##**kwargs === (add/remove/edit book, book_id, book_details)
    #def fine_user(self, **kwargs)
        ##**kwargs === (infringement, fine, user_id)


class Staff(Users):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def add_user(self, user_data):
        Customer(**user_data)
    #def delete_user(self, user_id)
    #def manage_books(self, **kwargs)
        ##**kwargs === (add/remove/edit book, book_id, book_details)
    #def fine_user(self, **kwargs)
        ##**kwargs === (infringement, fine, user_id)

class Books(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
