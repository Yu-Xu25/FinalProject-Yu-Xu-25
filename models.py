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
    comfort_level = db.Column(db.Integer, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Profile : id = {self.user_id})"

class WeatherForecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(200), nullable=True)
    temperature = db.Column(db.Float, nullable=False)
    feels_like = db.Column(db.Float, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    precipitation = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.Float, nullable=True)
    uv_index = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"WeatherForecast(city={self.city}, time={self.time}, condition={self.condition})"

# Sample Clothing Items (Predefined by the app)
class SampleClothingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  
    category = db.Column(db.String(50), nullable=False)  
    temperature_ranges = db.Column(db.String(100), nullable=False)
    precipitation_tag = db.Column(db.Boolean, nullable=False)
    wind_protection_tag = db.Column(db.Boolean, nullable=False)
    uv_protection_tag = db.Column(db.Boolean, nullable=False)
    layer_type = db.Column(db.String(50), nullable=True)  # base layer, mid layer or outer layer
    setting = db.Column(db.String(50), nullable=True)   # Indicates the clothing setting: "casual", "formal", "active", etc.

    def __repr__(self):
        return f"<SampleClothingItem {self.name}, {self.category}>"

# User's Custom Clothing Items (Editable by the user)
class UserClothingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  
    category = db.Column(db.String(50), nullable=False)  
    temperature_ranges = db.Column(db.String(100), nullable=False)
    precipitation_tag = db.Column(db.Boolean, nullable=False)
    wind_protection_tag = db.Column(db.Boolean, nullable=False)
    uv_protection_tag = db.Column(db.Boolean, nullable=False)
    layer_type = db.Column(db.String(50), nullable=True)  
    setting = db.Column(db.String(50), nullable=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<UserClothingItem {self.name}, {self.category}, User: {self.user_id}>"

