from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True) # set user id to be primary key
    username = db.Column(db.String(20), unique = True, nullable = True) # unique and nonempty username
    password = db.Column(db.String(50), unique = True, nullable = True)
    
    # relationship: each user has a profile, backref creates a virtual attribute user.profile
    profile = db.relationship('Profile', backref = 'user', uselist = False)

    def __repr__(self):
        return f"User : id = {self.id}, username = {self.username}"


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True) # set user id to be primary key
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(20), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    country = db.Column(db.String(50), nullable = False)
    sense_temp = db.Column(db.String(30), nullable = True)
    sense_light = db.Column(db.String(30), nullable = True)
    sense_humidity = db.Column(db.String(30), nullable = True)
    has_allegies = db.Column(db.String(10), nullable = True)
    has_asthma = db.Column(db.String(10), nullable = True)
    other = db.Column(db.String(200), nullable = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Profile : id = {self.user_id})"