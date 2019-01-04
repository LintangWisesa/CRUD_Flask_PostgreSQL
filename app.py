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

@app.route('/data', methods=['POST', 'GET'])
def data():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        name = body['name']
        age = body['age']

        data = User(name, age)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
            'name': name,
            'age': age
        })
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        # data = User.query.all()
        data = User.query.order_by(User.id).all()
        print(data)
        dataJson = []
        for i in range(len(data)):
            # print(str(data[i]).split('/'))
            dataDict = {
                'id': str(data[i]).split('/')[0],
                'name': str(data[i]).split('/')[1],
                'age': str(data[i]).split('/')[2]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson)

@app.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = User.query.get(id)
        print(data)
        dataDict = {
            'id': str(data).split('/')[0],
            'name': str(data).split('/')[1],
            'age': str(data).split('/')[2]
        }
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        delData = User.query.filter_by(id=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        newName = body['name']
        newAge = body['age']
        editData = User.query.filter_by(id=id).first()
        editData.name = newName
        editData.age = newAge
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})

if __name__ == '__main__':
    app.debug = True
    app.run()
