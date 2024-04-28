#!./new_env/bin/python3

from datetime import datetime
from sqlalchemy import Column, DATETIME, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from uuid import uuid4
import models


Base = declarative_base()


class Model(object):
    def __init__(self, **kwargs):
        if kwargs and len(kwargs) != 0:
            for key in kwargs:
                if key != "__class__":
                    setattr(self, key, kwargs[key])
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def save(self):
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        models.storage.delete(self)


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
    borrowed_books = relationship("Book", secondary='customer_books')
    role = Column(String(60))

    __limit = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_num_of_borrowed(self):
        return len(self.borrowed_books)

    def get_borrowed(self):
        return self.borrowed_books

    def borrow_book(self, book_id):
        lst = self.borrowed_books
        if len(lst) < self.__limit or lst is None:
            self.borrowed_books.append(book_id)
            models.storage.save()
            return True
        else:
            return False

    def return_book(self, book_id):
        self.borrowed_books.delete(book_id)
        models.storage.save()
        return True

    def pay_fine(self, amount):
        all_customers = models.storage.all(Customer)
        for key, value in all_customers.items():
            if key == self.id:
                paid_fine = value["fine"] - amount
                self.fine = paid_fine
                models.storage.save()

    def delete_account(self):
        models.storage.delete(self)

    def update_account(self, update_details):
        for key, value in update_details:
            self[key] = value
        models.storage.save()

    def fine_customer(self, fine):
        self.fine = fine


class Staff(Users, Base):

    __tablename__ = "staff"
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'latin1'}

    id = Column(String(256), primary_key=True)
    created_at = Column(DATETIME, default=datetime.now, nullable=False)
    updated_at = Column(DATETIME, default=datetime.now, nullable=False)
    first_name = Column(String(256))
    last_name = Column(String(256))
    email_address = Column(String(256))
    user_name = Column(String(256))
    password = Column(String(256))
    role = Column(String(60))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_user(self, **user_data):
        """ method to create a new user """
        if user_data["role"] == "Customer":
            new_customer = Customer(**user_data)
            new_customer.save()

    def delete_user(self, user_id):
        all_users = models.storage.all(Customer)
        for key, value in all_users.items():
            if key == user_id:
                value.delete()
                break

    def fine_user(self, **kwargs):
        fine = kwargs["fine"]
        all_users = models.storage.all(Customer)
        for key, value in all_users.items():
            if key == kwargs["user_id"]:
                value.fine_customer(fine)
                models.storage.save()
                break

    def add_book(self, **book_details):
        new_book = Books(**book_details)
        new_book.save()

    def remove_book(self, book_id):
        all_books = models.storage.all(Books)
        for key, value in all_books.items():
            if key == book_id:
                value.delete()
                break

    def update_book(self, **book_details):
        all_books = models.storage.all(Books)
        for key, value in all_books.items():
            if key == book_details["id"]:
                for key in book_details:
                    setattr(value, key, book_details[key])
                value.update_book()
                break


class Admin(Staff):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_user(self, **user_data):
        if user_data["role"] == "Admin":
            new_admin = Admin(**user_data)
            new_admin.save()
        elif user_data["role"] == "Staff":
            new_staff = Staff(**user_data)
            new_staff.save()
        else:
            new_customer = Customer(**user_data)
            new_customer.save()

    def delete_user(self, **kwargs):
        if kwargs["role"] == "Admin":
            all_users = models.storage.all(Admin)
            for key, value in all_users.items():
                if key == kwargs["id"]:
                    value.delete()
                    break
        elif kwargs["role"] == "Staff":
            all_users = models.storage.all(Staff)
            for key, value in all_users.items():
                if key == kwargs["id"]:
                    value.delete()
                    break
        else:
            all_users = models.storage.all(Customer)
            for key, value in all_users.items():
                if key == kwargs["id"]:
                    value.delete()
                    break


class Books(Model, Base):

    __tablename__ = "books"
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'latin1'}

    id = Column(String(256), primary_key=True)
    created_at = Column(DATETIME, default=datetime.now, nullable=False)
    updated_at = Column(DATETIME, default=datetime.now, nullable=False)
    title = Column(String(256))
    author = Column(String(256))
    publisher = Column(String(256))
    ISBN_Number = Column(Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_book(self, ):
        models.storage.save()


class CustomerBook(Base):

    __tablename__ = 'customer_books'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'latin1'}

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
