from flask import Flask
import os
app = Flask(__name__)

#specify the path to the DB 
curr_path = os.path.realpath(os.getcwd())
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s\\database.db'%(curr_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

