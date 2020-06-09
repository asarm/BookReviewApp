import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


DATABASE_URL = "postgres://ebpharyyuilerk:7189355070df9d885b5e3f7a1f24ad7518e9bc392dce3dd05e3f0f5ff8adca0c@ec2-54-75-246-118.eu-west-1.compute.amazonaws.com:5432/de6d4r723rdhcc"
# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


with open('books.csv','r') as file:
    reader = csv.reader(file)
    file.readline()
    for row in reader:
        db.execute('INSERT INTO books (isbn,title,author,year) VALUES (:isbn,:title,:author,:year)',
        {'isbn':row[0],'title':row[1],'author':row[2],'year':row[3]})
        db.commit()
        print(f'{row[1]} added!')

    print('Done!')
