from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Just avoids the warning message
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'  # location of database could be anywhere

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)
    age = db.Column(db.Integer)


@app.route('/<name>/<location>')
@cross_origin()
def index(name, location):
    user = User(name=name, location=location)
    db.session.add(user)
    db.session.commit()

    return '<h1>Added New User!</h1>'


# @app.route('/<name>')
# def get_user(name):
#     user = User.query.filter_by(name=name).first()
#
#     return f'<h1>The user is located in: {user.location}</h1>'


@app.route('/userAge')
@cross_origin()
def getAllAge():
    # user = User.query.getAll().first()
    resultproxy = db.engine.execute("Select * FROM User")  # Enter Query here

    data, rows = {}, []
    for rowproxy in resultproxy:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            data = {**data, **{column: value}}
        rows.append(data)

    ages = []
    names = []

    for user in rows:
        ages.append(user['age'])
        names.append(user['name'])

    # # using list comprehension
    agesStr = ','.join([str(elem) for elem in ages])
    namesStr = ','.join([str(elem) for elem in names])

    finalStr = agesStr + '\n' + namesStr
    return finalStr


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=50)
