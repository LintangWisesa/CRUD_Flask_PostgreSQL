from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/lin_flask'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    
    def __init__(self, email):
        self.email = email
    
    def __repr__(self):
        return '%s/%s' % (self.id, self.email)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/data', methods=['POST', 'GET', 'DELETE', 'PUT'])
def data():

    if request.method == 'POST':
        body = request.json
        print(body['email'])
        if not db.session.query(User).filter(User.email == body['email']).count():
            reg = User(body['email'])
            db.session.add(reg)
            db.session.commit()
            return 'Anda sukses nge-POST!'

    elif request.method == 'GET':
        data = User.query.all()
        print(data)
        dataJson = []
        for i in range(len(data)):
            # print(str(data[i]).split('/', 2))
            dataDict = {
                'id': str(data[i]).split('/', 2)[0],
                'email': str(data[i]).split('/', 2)[1]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson)

    elif request.method == 'DELETE':
        id = 2
        delData = User.query.filter_by(id=id).first()
        db.session.delete(delData)
        db.session.commit()
        return 'Anda sukses nge-DELETE!'

    else:
        body = request.json
        emailBaru = body['new_email']
        emailLama = body['old_email']
        editData = User.query.filter_by(email=emailLama).first()
        editData.email = emailBaru
        db.session.commit()
        return 'Anda sukses nge-PUT!'

if __name__ == '__main__':
    app.debug = True
    app.run()