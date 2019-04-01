from flask import Flask

app = Flask(__name__)

#specify the path to the DB 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\test\\python\\PythonFlask-WebServices\\database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

