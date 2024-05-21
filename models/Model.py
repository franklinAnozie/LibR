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
        models.storage.save()

    def new(self):
        models.storage.new(self)
        self.save()

    def delete(self):
        models.storage.delete(self)

    def update(self, update_details):
        update_details["updated_at"] = datetime.now()
        for key, value in update_details.items():
            setattr(self, key, value)
        self.save()


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
    borrowed_books = relationship("Books", secondary='customer_books')
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
            specific_book = models.storage.get(Books, book_id)
            if specific_book is not None:
                self.borrowed_books.append(specific_book)
                self.save()
                return True
            else:
                return False
        else:
            return False

    def return_book(self, book_id):
        specific_book = models.storage.get(Books, book_id)
        if specific_book is not None:
            self.borrowed_books.remove(specific_book)
        self.save()
        return True

    def pay_fine(self, amount):
        if self.fine is not None:
            self.fine -= amount
            self.save()
            return self.fine
        else:
            return False

    def delete_account(self):
        if self.get_num_of_borrowed > 0:
            return False
        else:
            self.delete()
            return True

    def update_account(self, update_details):
        self.update(update_details)

    def fine_customer(self, fine):
        self.fine = fine
        self.save()


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
            new_customer.new()
            new_customer.save()
            return new_customer

    def delete_user(self, **user_details):
        specific_user = None
        if user_details["role"] == "Customer":
            specific_user = models.storage.get(Customer, user_details["id"])
        if specific_user is not None:
            if specific_user.get_num_of_borrowed() == 0:
                specific_user.delete()
                return True
            else:
                return False
        else:
            return False

    def fine_user(self, **user_details):
        user = models.storage.get(Customer, user_details["id"])
        user.fine_customer(user_details["fine"])

    def add_book(self, **book_details):
        new_book = Books(**book_details)
        new_book.save()

    def remove_book(self, book_id):
        specific_book = models.storage.get(Books, book_id)
        if specific_book is not None:
            all_borrowed = models.storage.all(CustomerBook)
            for each_book in all_borrowed.values():
                if each_book.book_id == specific_book.id:
                    return False
            specific_book.delete()
            return True
        else:
            return False

    def update_book(self, book_details):
        specific_book = models.storage.get(Books, book_details["id"])
        specific_book.update(book_details)
        return True


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

    def delete_user(self, **user_details):
        specific_user = None
        if user_details["role"] == "Admin":
            specific_user = models.storage.get(Admin, user_details["id"])
        elif user_details["role"] == "Staff":
            specific_user = models.storage.get(Staff, user_details["id"])
        else:
            specific_user = models.storage.get(Customer, user_details["id"])
            if specific_user.get_num_of_borrowed() > 0:
                return False
        if specific_user is not None:
            specific_user.delete()
        else:
            return False


class Books(Model, Base):

    __tablename__ = "books"
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'latin1'}

    id = Column(String(256), primary_key=True)
    created_at = Column(DATETIME, default=datetime.now, nullable=False)
    updated_at = Column(DATETIME, default=datetime.now, nullable=False)
    title = Column(String(256))
    author = Column(String(256))
    publisher = Column(String(256))
    ISBN_Number = Column(String(256))
    borrowed_by = relationship("Customer", secondary='customer_books',
                               back_populates="borrowed_books", viewonly=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def delete_book(self):
        models.storage.delete(self)

    def get_borrowed_by(self):
        return self.borrowed_by


class CustomerBook(Base):

    __tablename__ = 'customer_books'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'latin1'}

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(256), ForeignKey('customers.id'))
    book_id = Column(String(256), ForeignKey('books.id'))
