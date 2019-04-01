# this file is renamed from books.py to app.py so that we can run flask run command to run the app
# if you want to keep the filename same, you need to run the below commands:
# set FLASK_APP=hello.py
# set FLASK_ENV=development
# flask run 
from flask import Flask, jsonify, request, Response
import json
from settings import *
from BookModel import *
from UserModel import *
from functools import wraps

import jwt
import datetime

app.config['SECRET_KEY'] = 'vnakka' #configure the app with the secret key

#POST /login     #this would fetch a jwt token with an expiration time of 500 seconds from now
@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    user_match = Users.username_password_match(username, password)
    if user_match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=500)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response(json.dumps({'error': 'username and passwords are not matching with the record in our DB. Please enter correct credentials'}), 401, mimetype="application/json") 


def token_required(f):
    @wraps(f)   #this will preserve the original func name as we decorate different routes
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            decode = jwt.decode(token, app.config['SECRET_KEY'])
            print(decode)
            return f(*args, **kwargs)
        except:
            return jsonify({'errror':'valid jwt token is not passed. Hence couldnot display the data'}), 401
    return wrapper

#this would fetch all the books
#GET /books?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoicGF5bG9hZCJ9.SePiJiKnHWTZjk0SvBPqkX9G_wtG9JqtNPKRrky8CDI   
@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()}) #convert list into json object

#Verify if the data sent by the user is a valid or not
def validBookObject(bookObject):
    if ('name' in bookObject and 'price' in bookObject and 'isbn' in bookObject):
        return True
    else:
        return False

#POST /books   #this would add a book to the existing collection of books
#{
#    'name': 'A',
#    'price': 6.99,
#    'isbn': 161351033251
#}

#POST /books
@app.route('/books', methods=["POST"])
@token_required
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", "201", mimetype="application/json")
        response.headers['Location'] = 'books/'+ str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMessage = {
            "error": "Invaid book object passed in the request",
            "helpString": "Data passed should be simiar to this {'name':'The Moonlight', 'price': 10.99, 'isbn':234234343445} "
        }
        response = Response(json.dumps(invalidBookObjectErrorMessage), status=400, mimetype="application/json")
        return response

#GET /books/9235632321353   #this would fetch a specific book from the books object
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value) #convert dict into json object

#sanitize the data sent by the user for the put request
def validPutRequestData(request_data):
    if ('name' in request_data and 'price' in request_data):
        return True
    else:
        return False

#PUT /books/9235632321353   #this would update the existing book from the book collection
#{
#    'name': 'Harry Potter',
#    'price': 10.99
#}
@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
    update_request = request.get_json()

    #sanitize the input we are receiving as part of the request
    if(not validPutRequestData(update_request)):
        invalidBookObjectErrorMessage = {
            "error": "valid book object must be passed in the request",
            "helpMessage": "data passed should be in this format {'name':'Harry Potter','price':11.99}"
        }
        response = Response(invalidBookObjectErrorMessage, status=400, mimetype="application/json")
        return response

    Book.replace_book(isbn, update_request['name'], update_request['price'])
    response = Response("", status=204)
    return response

#sanitize the data sent by the user for the put request
def validPatchRequestData(request_data):
    if ('name' in request_data or 'price' in request_data):
        return True
    else:
        return False

#PATCH /books/9235632321353   #this would update only the required keys of a book sent by the client
#{
#   'name': "Harry Potter and the Chamber of secrets"
#}
@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()
    
    if 'name' in request_data:
        Book.update_book_name(isbn, request_data['name']) 
    if 'price' in request_data:
        Book.update_book_price(isbn, request_data['price']) 

    #santize the input we are receiving as part of the request
    if(not validPatchRequestData(request_data)):
        invalidBookObjectErrorMessage = {
            "error": "valid book object must be passed in the request",
            "helpMessage": "data passed should have either {'name':'Harry Potter'} or {'price':11.99} or both" 
        }
        response = Response(invalidBookObjectErrorMessage, status=400, mimetype="application/json")
        return response
    else:
        response = Response("", status=204)
        response.headers['Location'] = '/books/' + str(isbn)
        return response

#DELETE /books/9235632321353   #this would delete the book entry from books collection by accepting the isbn
@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        response = Response("", status=204)
        return response
    invalidBookObjectErrorMessage = {
        "error": "Book with isbn provided is not found. Hence, cannot delete the book"
    }
    response = Response(json.dumps(invalidBookObjectErrorMessage), status=400, mimetype="application/json")
    return response

app.run(port=5000)