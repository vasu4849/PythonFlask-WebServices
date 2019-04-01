from flask import Flask, jsonify, request, Response
import json
from settings import *

"""
books= [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 978115161320
    },
    {
        'name': 'The Cat in the Hat',
        'price': 5.99,
        'isbn': 9235632321353
    },
    {   'name': 'Lord of the Rings',
        'price': 10.99,
        'isbn': 84651321333132
    }
]
"""

#GET /books   #this would fetch all the books
@app.route('/books')
def get_books():
    return jsonify({'books':books}) #convert list into json object

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
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn'] 
        }
        books.insert(0, new_book) #insert the new book at the first value
        response = Response("", "201", mimetype="application/json")
        response.headers['Location'] = 'books/'+ str(new_book['isbn']) 
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
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value = {
               'name': book['name'],
               'price': book['price']    
            }            
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

    new_book = {
        'name': update_request['name'],
        'price': update_request['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        if(book['isbn'] == isbn):
            books[i] = new_book   
        i+=1
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
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if 'name' in request_data:
        updated_book['name'] = request_data['name']
    if 'price' in request_data:
        updated_book['price'] = request_data['price']

    #santize the input we are receiving as part of the request
    if(not validPatchRequestData(request_data)):
        invalidBookObjectErrorMessage = {
            "error": "valid book object must be passed in the request",
            "helpMessage": "data passed should have either {'name':'Harry Potter'} or {'price':11.99} or both" 
        }
        response = Response(invalidBookObjectErrorMessage, status=400, mimetype="application/json")
        return response
    else:
        for book in books:
            if(book['isbn'] == isbn):
                book.update(updated_book)
        response = Response("", status=204)
        response.headers['Location'] = '/books/' + str(isbn)
        return response

#DELETE /books/9235632321353   #this would delete the book entry from books collection by accepting the isbn
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    request_body = request.get_json()
    i = 0
    for book in books:
        if(book['isbn']== isbn):
            books.pop(i)
            response = Response("", status=204)
            return response
        i+=1
    invalidBookObjectErrorMessage = {
        "error": "Book with isbn provided is not found. Hence, cannot delete the book"
    }
    response = Response(json.dumps(invalidBookObjectErrorMessage), status=400, mimetype="application/json")
    return response

app.run(port=5000)