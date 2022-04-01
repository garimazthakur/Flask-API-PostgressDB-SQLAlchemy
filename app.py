from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/catalouge"

db = SQLAlchemy(app)
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    published = db.Column(db.String(255)) 

    def __init__(self, name, author, published):
        self.name = name
        self.author = author
        self.published = published
        
@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        allbooks = Book.query.all()
        output = []
        for book in allbooks:
            currbook = {}
            currbook['name'] = book.name
            currbook['author'] = book.author
            currbook['published'] = book.published
            output.append(currbook)
        return jsonify(output)   

    # POST a data to database
    if request.method == 'POST':
        body = request.json
        name= body['name']
        author= body['author']
        published=body['published']

        data = Book(name, author, published)
        db.session.add(data)
        db.session.commit()
        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
            'name': name,
            'author': author,
            'published': published
        })
@app.route('/data/<int:id>', methods=['GET','DELETE', 'PUT'])
def onedata(id):

    if request.method == 'GET':
        print("-----------------")
        data = Book.query.get(id)

        dataDict ={
            "id":data.id,
            "name": data.name,
            "author": data.author,
            "published":data.published
        }

        return jsonify(dataDict)

    if request.method == 'DELETE':
        # delData = Book.query.filter_by(id=id).first()
        delData = Book.query.get(id)
        db.session.delete(delData)
        db.session.commit()
        return jsonify(delData)
        # return jsonify(delData)
    if request.method == 'PUT':
        body = request.json
        newName = body['name']
        newAuthor = body['author']
        newPublished = body['published']

        editData = Book.query.filter_by(id=id).first()

        editData.name = newName
        editData.author = newAuthor
        editData.published= newPublished

        print(editData.name)
        print(editData.author)
        print(editData.published)
        db.session.add(editData)
        db.session.commit()
        # return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})
        # return jsonify(editData)
        print("###########################################")
        print(type(editData))
        return jsonify("{}")

if __name__ == '__main__':
    app.run(port=5007, debug=True)
