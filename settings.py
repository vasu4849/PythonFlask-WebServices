from flask import Flask

app = Flask(__name__)

#specify the path to the DB 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Automation\\My work\\python\\PythonFlask\\database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

