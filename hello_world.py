#-------------------------------------------------------------------------------
# Name:        hello_world
# Purpose:
#
# Author:      vnakka
#
# Created:     11/03/2019
# Copyright:   (c) vnakka 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------


from flask import Flask

app = Flask(__name__)
print(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

app.run(port=5000)
