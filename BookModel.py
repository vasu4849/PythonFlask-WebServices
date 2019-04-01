from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

#create the Db object for SQLAlchemy
db = SQLAlchemy(app)

class Book(db.Model):
    #we have the DB name: database.db defined in settings.py. If not, you can specify it here as well
    __tablename__ = 'books'     #this is the name of the DB table on sqllite DB

    #we are going to create the columns here
    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isbn= db.Column(db.Integer)

    #add a book to the Db table books
    def add_book(_name, _price, _isbn):
        new_book = Book(name=_name, price= _price, isbn=_isbn)
        db.session.add(new_book)
        db.session.commit()
    
    #converts the object into json format 
    def json(self):
        return {'name': self.name, 'price':self.price, 'isbn':self.isbn}

    
    #get all books from the Db table: books
    def get_all_books():
        return [Book.json(book) for book in Book.query.all()]          #query method is defined in the base class: db.Model and it would get the data from DB

    #get a book from the isbn number provided
    def get_book(_isbn):
        return Book.query.filter_by(isbn=_isbn).first()

    #delete the book from the DB with the isbn number provided
    def delete_book(_isbn):
        #this would fetch the records matching with the specific isbn number and delete those ones
        is_successful = Book.query.filter_by(isbn=_isbn).delete() 
        db.session.commit()
        return bool(is_successful)
    
    #update the price for the book with a specific isbn number provided
    def update_book_price(_isbn, _price):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        #the below command would update the price for the fetched records
        book_to_update.price = _price
        db.session.commit()

    #update the price for the book with a specific isbn number provided
    def update_book_name(_isbn, _name):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.name = _name
        db.session.commit()

    #replace a book with name and price fields with the isbn provided
    def replace_book(_isbn, _name, _price):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.name = _name
        book_to_update.price = _price
        db.session.commit()

    #print the records in the friendly format
    def __repr__(self):
        book_object = {
            'name': self.name,
            'price': self.price,
            'isbn': self.isbn
        }
        return json.dumps(book_object) 

    
    