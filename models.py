from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# User data
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True) # set user id to be primary key
    username = db.Column(db.String(20), unique = True, nullable = True) # unique and nonempty username
    password = db.Column(db.String(50), unique = True, nullable = True)
    
    # relationship: each user has a profile, backref creates a virtual attribute user.profile
    profile = db.relationship('Profile', backref = 'user', uselist = False)

    def __repr__(self):
        return f"User : id = {self.id}, username = {self.username}"

# User Profile Data
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True) # set user id to be primary key
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(20), nullable = False)
    location_zip = db.Column(db.String(10), nullable=True)
    location_city = db.Column(db.String(100), nullable=True)
    location_latitude = db.Column(db.String, nullable=True)
    location_longitude = db.Column(db.String, nullable=True)
    comfort_level = db.Column(db.Integer, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Profile : id = {self.user_id})"


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

# User's Location
class UserLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_zip = db.Column(db.String(10), nullable=True)
    location_city = db.Column(db.String(100), nullable=True)
    location_latitude = db.Column(db.String(20), nullable=True)
    location_longitude = db.Column(db.String(20), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def get_location_name(self):
        if self.location_city:
            return self.location_city
        elif self.location_zip:
            return self.location_zip
        elif self.location_latitude is not None and self.location_longitude is not None:
            return f"{self.location_latitude},{self.location_longitude}"
        return "Unknown Location"
    
    def __repr__(self):
        return f"<UserLocation {self.id} - User {self.user_id}>"
