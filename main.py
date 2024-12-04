# render HTML templates, redirecting user to another page through url
from flask import Flask, render_template, request, redirect, url_for
# provide user session management, adds useful methods for user management (like is_authenticated, is_active, get_id())
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# allow hashing passwords for security
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import secrets
from datetime import timedelta

from forms import *
from models import *
from algorithms import *


secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # set up a SQLite database to use
# control how long users remain logged in before being automatically logged out
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15) 
# allows the class to map to a database table
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect to login page if not logged in


# python decorator that flask uses to connect url end point with code-containing functions
# home page
@app.route('/')
def home():
    # User is logged in
    if current_user.is_authenticated:
        
        primary_location = UserLocation.query.filter_by(user_id=current_user.id, is_primary=True).first()
        
        location_name = primary_location.get_location_name()
         # Get the weather data for the user's specified location
        weather_data, alert = get_weather(location_name)
        
        condition = weather_data.get("condition", {}).get("text")
        temperature_c = weather_data.get("temp_c")
        temperature_f = weather_data.get("temp_f")
        feels_like_c = weather_data.get("feelslike_c")
        feels_like_f = weather_data.get("feelslike_f")
        wind_speed_kph = weather_data.get("wind_kph")
        wind_speed_mph = weather_data.get("wind_mph")
        precipitation_mm = weather_data.get("precip_mm")
        precipitation_in = weather_data.get("precip_in")
        humidity = weather_data.get("humidity")
        
        # Fetch customized outfit recommendations based on user profile preferences
        
        outfit_recommendations = get_outfit_recommendations(weather_data, current_user.profile)
        #outfit_recommendations = []
        return render_template('home.html', 
                               location_name = location_name,
                               username=current_user.username,  # Display username
                               alert=alert, condition=condition,
                               temperature_c=temperature_c, feels_like_c=feels_like_c,
                               temperature_f=temperature_f, feels_like_f=feels_like_f,
                               wind_speed_kph=wind_speed_kph, wind_speed_mph=wind_speed_mph,
                               precipitation_mm=precipitation_mm, precipitation_in=precipitation_in,
                               humidity=humidity, recommendations=outfit_recommendations)
    else:
        # User is not logged in, show default weather for Chicago
        city_name = "Chicago"  # Default city
        weather_data, alert = get_weather(city_name=city_name)

        condition = weather_data.get("condition", {}).get("text")
        temperature_c = weather_data.get("temp_c")
        temperature_f = weather_data.get("temp_f")
        feels_like_c = weather_data.get("feelslike_c")
        feels_like_f = weather_data.get("feelslike_f")
        wind_speed_kph = weather_data.get("wind_kph")
        wind_speed_mph = weather_data.get("wind_mph")
        precipitation_mm = weather_data.get("precip_mm")
        precipitation_in = weather_data.get("precip_in")
        humidity = weather_data.get("humidity")
        

        # Default outfit recommendations based on Chicago's weather
        outfit_recommendations = get_default_outfit_recommendations(weather_data)
        #outfit_recommendations = []

        return render_template('home.html',
                               condition=condition,
                               temperature_c=temperature_c, feels_like_c=feels_like_c,
                               temperature_f=temperature_f, feels_like_f=feels_like_f,
                               wind_speed_kph=wind_speed_kph, wind_speed_mph=wind_speed_mph,
                               precipitation_mm=precipitation_mm, precipitation_in=precipitation_in,
                               humidity=humidity, recommendations=outfit_recommendations)

# Create tables and populate sample data during application setup
@app.before_request
def setup():
        #db.drop_all()
        db.create_all()
        populate_sample_data()

# profile creation 
@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
        return render_template('profile.html', profile = current_user.profile)

# edit profile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UserProfileForm(obj=current_user.profile)

    if form.validate_on_submit():
        # Update user profile with the form data
        current_user.profile.age = form.age.data
        current_user.profile.gender = form.gender.data
        current_user.profile.location_zip = form.location_zip.data \
                if form.location_zip.data else None
        current_user.profile.location_city = form.location_city.data \
                if form.location_city.data else None
        current_user.profile.location_latitude = form.location_latitude.data \
                if form.location_latitude.data else None
        current_user.profile.location_longitude = form.location_longitude.data \
                if form.location_longitude.data else None
        current_user.profile.comfort_level = int(form.comfort_level.data)

        db.session.commit() # commit profile change

        primary_location = UserLocation.query.filter_by(user_id=current_user.id, is_primary=True).first()
        # If pimary location is already set, change it into the entry in edit profile
        if primary_location:
            primary_location.location_zip = form.location_zip.data \
                if form.location_zip.data else None
            primary_location.location_city = form.location_city.data \
                if form.location_city.data else None
            primary_location.location_latitude = form.location_latitude.data \
                if form.location_latitude.data else None
            primary_location.location_longitude = form.location_longitude.data \
                if form.location_longitude.data else None
        else:
            # Create a new primary location
            primary_location = UserLocation(
                user_id=int(current_user.id),
                location_zip=form.location_zip.data if form.location_zip.data else None,
                location_city=form.location_city.data if form.location_city.data else None,
                location_latitude=form.location_latitude.data if form.location_latitude.data else None,
                location_longitude=form.location_longitude.data if form.location_longitude.data else None,
                is_primary=True
            )
            db.session.add(primary_location)

        db.session.commit() # commit location change
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form=form)


@app.route('/manage_locations', methods=['GET', 'POST'])
@login_required
def manage_locations():
    form = LocationForm()
    user_locations = UserLocation.query.filter_by(user_id=current_user.id).all()

    if form.validate_on_submit():
        if form.is_primary.data:
            # Set all other locations as non-primary
            UserLocation.query.filter_by(user_id=current_user.id, is_primary=True).update({"is_primary": False})
        # Add new location
        new_location = UserLocation(
            user_id=current_user.id,
            location_zip=form.location_zip.data,
            location_city=form.location_city.data,
            location_latitude=form.location_latitude.data,
            location_longitude=form.location_longitude.data,
            is_primary=form.is_primary.data
        )
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('manage_locations'))

    return render_template('manage_locations.html', form=form, locations=user_locations)


# delete location
@app.route('/delete_location/<int:location_id>', methods=['GET', 'POST'])
@login_required
def delete_location(location_id):
    location = UserLocation.query.get_or_404(location_id)
    if location.user_id == current_user.id:
        db.session.delete(location)
        db.session.commit()

    return redirect(url_for('manage_locations'))

# Set a location as primary to be displayed at home page
@app.route('/set_primary_location/<int:location_id>', methods=['GET', 'POST'])
@login_required
def set_primary_location(location_id):
    # Set all other locations to non-primary
    UserLocation.query.filter_by(user_id=current_user.id, is_primary=True).update({"is_primary": False})

    # Set the selected location as primary
    location = UserLocation.query.get_or_404(location_id)
    if location.user_id == current_user.id:
        location.is_primary = True
        db.session.commit()

    return redirect(url_for('manage_locations'))

# Add new item in the user's wardrobe
@app.route('/manage_wardrobe', methods=['GET', 'POST'])
@login_required
def manage_wardrobe():
    form = ManageWardrobeForm()

    if form.validate_on_submit():
        # Convert list of temperature ranges to comma-separated string
        temperature_ranges_str = ",".join(form.temperature_ranges.data) \
                if form.temperature_ranges.data else ""

        # Create new UserClothingItem with correct boolean values from the form
        new_item = UserClothingItem(
            name=form.name.data,
            category=form.category.data,
            temperature_ranges=temperature_ranges_str,
            precipitation_tag=form.precipitation_tag.data,
            wind_protection_tag=form.wind_protection_tag.data,
            uv_protection_tag=form.uv_protection_tag.data,
            layer_type=form.layer_type.data,
            setting=form.setting.data,
            user_id=current_user.id
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('manage_wardrobe'))

    wardrobe_items = UserClothingItem.query.filter_by(user_id=current_user.id).all()

    return render_template('manage_wardrobe.html', form=form, wardrobe_items=wardrobe_items)

# Edit an item info in user's wardrobe
@app.route('/edit_wardrobe_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_wardrobe_item(item_id):
    item = UserClothingItem.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        return redirect(url_for('manage_wardrobe'))

    form = ManageWardrobeForm(obj=item)
    form.temperature_ranges.data = item.temperature_ranges.split(",") \
        if item.temperature_ranges else []

    if form.validate_on_submit():
        # Update the item with correct boolean values from the form
        item.name = form.name.data
        item.category = form.category.data
        item.temperature_ranges = ",".join(form.temperature_ranges.data) \
                if form.temperature_ranges.data else ""
        item.precipitation_tag = form.precipitation_tag.data
        item.wind_protection_tag = form.wind_protection_tag.data
        item.uv_protection_tag = form.uv_protection_tag.data
        item.layer_type = form.layer_type.data
        item.setting = form.setting.data

        db.session.commit()
        return redirect(url_for('manage_wardrobe'))

    return render_template('edit_wardrobe_item.html', form=form)


# delete a wardrobe item
@app.route('/delete_wardrobe_item/<int:item_id>', methods=['POST'])
@login_required
def delete_wardrobe_item(item_id):
    item = UserClothingItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        return redirect(url_for('manage_wardrobe'))

    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('manage_wardrobe'))


# New user registration
@app.route('/register', methods = ['GET', 'POST'])
def register():
        form = RegistrationForm()
        if form.validate_on_submit():
                hashed_password = generate_password_hash(form.password.data)
                user = User(username = form.username.data, password = hashed_password)

                profile = Profile(
                        age = form.age.data, gender = form.gender.data,
                        location_zip = form.location_zip.data, 
                        location_city = form.location_city.data,
                        location_latitude = form.location_latitude.data,
                        location_longitude = form.location_longitude.data,
                        comfort_level = int(form.comfort_level.data)
                )
                db.session.add(user)
                db.session.commit()  # commits both the user and profile to the database
                
                user.profile = profile
                db.session.add(profile)
                db.session.commit() # add user object in the database

                # populate user wardrobe with sample items
                populate_user_wardrobe(user.id)

                # add a location for user
                if form.location_zip.data or form.location_city.data or \
                        (form.location_latitude.data and form.location_longitude.data):
                        new_location = UserLocation(
                                user_id = int(user.id),
                                location_zip=form.location_zip.data \
                                        if form.location_zip.data else None,
                                location_city=form.location_city.data \
                                        if form.location_city.data else None,
                                location_latitude=form.location_latitude.data \
                                        if form.location_latitude.data else None,
                                location_longitude=form.location_longitude.data \
                                        if form.location_longitude.data else None,
                                is_primary=True
                        )
                        db.session.add(new_location)
                        db.session.commit()
                

                login_user(user) # log the user in
                return redirect(url_for('home'))
        return render_template('register.html', form = form)
# load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# log in a user
@app.route('/login', methods = ['GET', 'POST'])
def login():
        form = LoginForm()
        if form.validate_on_submit():
                user = User.query.filter_by(username = form.username.data).first()
                if user is None:
                        print("User not found.")  # Debugging: user not found
                if user and check_password_hash(user.password, form.password.data):
                        print("Password matched.")  # Debugging: password matched
                        login_user(user)
                        print("User logged in.")  # Debugging: user logged in
                        return redirect(url_for('home'))
                else:
                        print("Password didn't match.")  # Debugging: password didn't match
        return render_template('login.html', form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# weather api intergration
def get_weather(city_name=None, zipcode=None, latitude=None, longitude=None):
        api_url = "http://api.weatherapi.com/v1/forecast.json"
        api_key = "7ea62c83afb24f108ea225710242211"
        days = 1

        # Check if any required info is present
        if zipcode != None:
              q = zipcode
        elif latitude != None and longitude != None:
              q = f"{latitude},{longitude}"
        elif city_name != None:
              q = city_name
        else:
              return "Error: Please provide at least one form of location."
              
        # Make the API request
        response = requests.get(f"{api_url}?key={api_key}&q={q}&days={days}&aqi=no&alerts=yes")

        if response.status_code == 200:
                data = response.json()
        else:
                print("Error fetching weather data: ", response.status_code)

        current_weather = data.get("current", {})

                 
        # Extract alert data, display as headline if there's any severe weather should be alerted.
        alerts = data.get("alerts", {}).get("alert", [])
        alert_headline = alerts[0].get("headline") if alerts else None

        return current_weather, alert_headline


if __name__ == "__main__":
        app.run(host="127.0.0.1", port=8080, debug=True)
