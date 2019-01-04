from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import yaml

app = Flask(__name__)
db_config = yaml.load(open('database.yaml'))
app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri'] 
db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.String(255))
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return '%s/%s/%s' % (self.id, self.name, self.age)

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
