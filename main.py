import os
import urllib.request
from flask import Flask, jsonify, redirect, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/catalouge1"
UPLOAD_FOLDER = "/home/softuvo/Garima/Flask Practice/Flask_practice/files/files_1"

db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Book(db.Model):
    __tablename__ = 'books1'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    published = db.Column(db.String(255)) 
    store = db.Column(db.String())


    def __init__(self, name, author, published, store, photo):
        self.name = name
        self.author = author
        self.published = published
        self.store = store

@app.route('/upload', methods = ['POST'])   
def upload():                         #This function will help you in uploading the files to the database
    file = request.files['inputFile']
    name = request.form['name']
    author = request.form['author']
    published = request.form['published']
    # rs_username = request.form['txtusername']
    filename = secure_filename(file.filename)
    if file and allowed_file(file.filename):
       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       newFile = Book(store=file.filename, name= name,author=author, published=published)
       db.session.add(newFile)
       db.session.commit()

    return jsonify("{}")
    

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
        return jsonify("{}")
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
        # print(type(editData))
        return jsonify("{}")

if __name__ == '__main__':
    app.run(port=5007, debug=True)
