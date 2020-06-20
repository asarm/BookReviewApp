import os

from flask import Flask, session, render_template, request, redirect, url_for, flash, message_flashed
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Check for environment variable
"""if not ("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")"""

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


DATABASE_URL = "postgres://ebpharyyuilerk:7189355070df9d885b5e3f7a1f24ad7518e9bc392dce3dd05e3f0f5ff8adca0c@ec2-54-75-246-118.eu-west-1.compute.amazonaws.com:5432/de6d4r723rdhcc"
# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

class Book():
    def __init__(self,isbn,title,author):
        self.isbn = isbn
        self.title = title
        self.author = author
    def __str__(self):
        return (f'{self.isbn} {self.author} {self.title}')
class Review():
    def __init__(self,username,comment,rating,isbn):
        self.username = username
        self.comment = comment
        self.rating = rating
        self.isbn = isbn

@app.route("/")
def index():
    if session.get('username') == None:
        flash('You have to login')
        return redirect(url_for('login'))

    username = session['username']
    books = db.execute("SELECT id, isbn, author, title FROM books").fetchall()

    first_books = []
    count = 0
    for book in books:
        first_books.append(book)
        count+=1
        if count == 20:
            break

    return render_template('home.html',username=username,books=books,first_books=first_books)

#Register
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        register_username = request.form.get('username')
        register_password = request.form.get('password')
        query = 'SELECT username FROM users WHERE username = :username'

        if db.execute(query, {'username': register_username}).first():
            flash('Username is already exist')
            return render_template('register.html')
        else:
            flash('Registration is successful')
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                       {"username": register_username, "password": register_password})
            db.commit()
            return redirect(url_for('login'))

#Login
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        login_username = request.form.get('username')
        login_password = request.form.get('password')
        session.clear()
        user = db.execute("SELECT username,password FROM users WHERE (username = :username AND password = :password)",
                {'username':login_username,'password':login_password}).first()
        if user == None:
            print('Invalid user')
            flash('Wrong username or password')
            return render_template('login.html')
        else:
            session['username'] = login_username
            return redirect(url_for('index'))

#Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('login')

#Detail
@app.route('/detail/<string:book_isbn>',methods=['GET','POST'])
def detail(book_isbn):
    if session.get('username') == None:
        return redirect(url_for('login'))
    apikey = '9TI4CoND28j0LEXkBRApw'
    url2 = f'https://www.goodreads.com/book/isbn/{book_isbn}?key={apikey}'
    response = requests.get(url2)
    soup = BeautifulSoup(response.content, "lxml-xml")
    rating = soup.find('average_rating').text
    year = (soup.find('publication_year').text)
    rating_num = float(rating)
    username = session['username']
    book = db.execute("SELECT id, isbn, author, title FROM books WHERE isbn = :isbn ",{'isbn':book_isbn}).fetchone()

    reviews = db.execute("SELECT * FROM reviews WHERE isbn=:isbn",{'isbn':book_isbn}).fetchall()
    user_check = db.execute("SELECT isbn FROM reviews WHERE username=:username AND isbn=:isbn",{'username':username,'isbn':book_isbn}).fetchone()

    control = False
    if user_check == None:
        control = True

    review_list = []
    for i in range(len(reviews)):
        review = Review(reviews[i][0],reviews[i][1],reviews[i][2],reviews[0][3])
        review_list.append(review)

    if request.method == "POST":
        if control == False:
            flash("You can't review more than one")
        else:
            review_username = username
            review_comment = request.form.get('review')
            review_rating = request.form.get('rating')

            db.execute("INSERT INTO reviews (username,comment,rating,isbn) VALUES (:username,:comment,:rating,:isbn)",
                               {"username":review_username,"comment":review_comment,"rating":review_rating,"isbn":book_isbn})
            db.commit()
            flash('Your review submitted')
            return render_template('detail.html', book=book, username=username, rating=rating,rating_num=rating_num, review_list=review_list)
    return render_template('detail.html',book=book,username=username,year=year,rating=rating,rating_num=rating_num,review_list=review_list)

#Search
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        search_key = request.form.get('query')
        search = '%' + search_key + '%'
        #query = db.execute("SELECT * FROM books WHERE title LIKE :search ",{"search":search}).fetchall()
        query = db.execute("SELECT * FROM books WHERE (isbn LIKE :search OR title LIKE :search OR author LIKE :search)",{"search":search}).fetchall()
        '''db.execute("SELECT isbn,title,author,year FROM books WHERE title LIKE :query OR author LIKE :query  OR isbn LIKE :query",
            {"query": query.title()}).fetchall()'''
        books = []
        for index,book in enumerate(query):
            book = Book(query[index][1], query[index][2], query[index][3])
            books.append(book)
        total_result = len(books)

        if session.get('username'):
            username = session['username']
            return render_template('results.html',books=books,username=username,total_result=total_result)

        else:
            flash('You have to sign in to search a book')
            return redirect('login')

@app.route('/api/<string:isbn>')
def api(isbn):
    apikey = '9TI4CoND28j0LEXkBRApw'
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn",{'isbn':isbn}).fetchone()
    try:
        url2 = f'https://www.goodreads.com/book/isbn/{isbn}?key={apikey}'
        response = requests.get(url2)
        soup = BeautifulSoup(response.content, "lxml-xml")
        rating = soup.find('average_rating').text
        year = (soup.find('publication_year').text)
        review_count = (soup.find('reviews_count').text)
        return render_template('api.html',book = book,rating=rating,review_count=review_count,year=year)
    except:
        return render_template('404.html')
