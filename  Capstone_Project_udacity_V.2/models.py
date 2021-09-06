from sqlalchemy import Column, String, create_engine, Integer, Date
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json
import os


database_path = "postgres://qmuctnxsjzynmq:caaa92f73f104bc8eaf93ab5b71a13adec2d14616f4eac78575a109a0a6e4896@ec2-52-70-67-123.compute-1.amazonaws.com:5432/d5o744grfo2435"
# database_path = "postgres:///m_db"
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()

# def db_insert_all():
#     db.drop_all()
#     db.create_all()
#     add_actor = Actor('atheer', 'Female', '20')
#     add_movie = Movie('hloe word ', date.today())
#     add_actor.insert()
#     add_movie.insert()
#     db.session.commit()

'''
Actor
'''

class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, gender, age):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

'''
Movie
'''

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
