import os
import urllib.request
from flask_appbuilder.models.mixins import ImageColumn
from flask import Flask, jsonify, redirect, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/catalouge2"
UPLOAD_FOLDER = "/home/softuvo/Garima/Flask Practice/Flask_practice/files/files_2"

db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
  
def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Book(db.Model):
    __tablename__ = 'book_store'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    published = db.Column(db.String(255)) 
    file = db.Column(db.String())
    photo = db.Column(ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)))

    def __init__(self, name, author, published, file, photo):
        self.name = name
        self.author = author
        self.published = published
        self.file = file
        self.photo = photo

@app.route('/upload', methods = ['POST'])   
def upload():                         #This function will help you in uploading the files to the database
    file = request.files['inputFile']
    name = request.form['name']
    author = request.form['author']
    published = request.form['published']
    file_path = request.form['photo']
    # rs_username = request.form['txtusername']
    filename = secure_filename(file.filename)
    if file and allowed_file(file.filename):
       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       print(file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) )
   

       f = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
       for fi in f:
           print(fi, end = "")
           
    #    f = file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
       

       print("++++++++++++++++++file_path+++++++++++++++++++")
       print(file_path)
    #    file_path1 = os.getcwd(file_path)
    #    print(file_path1)
    #    newFile = Book(store=file.filename, name=name, author=author, published=published, photo=photo)
       newFile = Book(file=file.filename,name= name,author=author, published=published, photo = [fi ])
       
       db.session.add(newFile)
       db.session.commit()
    return jsonify("{}")

if __name__ == '__main__':
    app.run(port=5008, debug=True)
