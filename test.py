#Verify if the data sent by the user is a valid or not 
def validBookObject(bookObject):
    if ('name' in bookObject and 'price' in bookObject and 'isbn' in bookObject):
        return True
    else:
        return False

valid_object = {
    "name": "Harry Potter",
    "price": 7.99,
    "isbn": 418461516547862
}

missing_name = {
    "price": 7.99,
    "isbn": 418461516547862
}

missing_price = {
    "name": "Harry Potter",
    "isbn": 418461516547862
}

missing_isbn = {
    "name": "Harry Potter",
    "price": 7.99
}

empty_book = {}