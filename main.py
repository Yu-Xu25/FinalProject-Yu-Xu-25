# render HTML templates, redirecting user to another page through url
from flask import Flask, render_template, request, redirect, url_for
# provide user session management, adds useful methods for user management (like is_authenticated, is_active, get_id())
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# allow interact with the database using Python classes instead of writing SQL queries
from flask_sqlalchemy import SQLAlchemy
# allow hashing passwords for security
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import secrets

from forms import *
from models import *
from algorithms import *


secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # set up a SQLite database to use
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# allows the class to map to a database table
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect to login page if not logged in


# python decorator that flask uses to connect url end point with code-containing functions
@app.route('/')
def home():
    if current_user.is_authenticated:
        # User is logged in
        city = current_user.profile.city  # Fetch the user's city from their profile
        weather_data, alert = get_weather(city)  # Get weather data for the user's location
        
        condition = weather_data.get("condition", {}).get("text")
        temperature_c = weather_data.get("temp_c")
        feels_like = weather_data.get("feelslike_c")
        wind_speed_kph = weather_data.get("wind_kph")
        precipitation_mm = weather_data.get("precip_mm")
        visibility_km = weather_data.get("vis_km")
        uv_index = weather_data.get("uv")
        humidity = weather_data.get("humidity")
        
        # Fetch customized outfit recommendations based on user profile preferences
        
        #outfit_recommendations = get_outfit_recommendations(weather_data, current_user.profile)
        outfit_recommendations = []
        return render_template('home.html', 
                               username=current_user.username,  # Display username
                               alert=alert,
                               condition=condition,
                               temperature=temperature_c,
                               feels_like=feels_like,
                               wind_speed=wind_speed_kph,
                               precipitation=precipitation_mm,
                               visibility=visibility_km,
                               uv_index=uv_index,
                               humidity=humidity,
                               outfit_recommendations=outfit_recommendations)
    else:
        # User is not logged in, show default weather for Chicago
        city = "Chicago"  # Default city
        weather_data, alert = get_weather(city)

        condition = weather_data.get("condition", {}).get("text")
        temperature_c = weather_data.get("temp_c")
        feels_like = weather_data.get("feelslike_c")
        wind_speed_kph = weather_data.get("wind_kph")
        precipitation_mm = weather_data.get("precip_mm")
        visibility_km = weather_data.get("vis_km")
        uv_index = weather_data.get("uv")
        humidity = weather_data.get("humidity")
        

        # Default outfit recommendations based on Chicago's weather
        # Call this function once to populate the database
        populate_sample_data()
        #outfit_recommendations = get_default_outfit_recommendations(weather_data)
        outfit_recommendations = []

        return render_template('home.html',
                               condition=condition,
                               temperature=temperature_c,
                               feels_like=feels_like,
                               wind_speed=wind_speed_kph,
                               precipitation=precipitation_mm,
                               visibility=visibility_km,
                               uv_index=uv_index,
                               humidity=humidity,
                               outfit_recommendations=outfit_recommendations)

# Create tables and populate sample data during application setup
@app.before_first_request
def setup():
        #db.drop_all()
        db.create_all()
        populate_sample_data()

# profile creation 
@app.route('/profile', methods = ['GET', 'POST'])
def profile():
        user_profile = current_user.profile
        return render_template('profile.html', profile = user_profile)

# edit profile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UserProfileForm(obj=current_user.profile)

    if form.validate_on_submit():
        # Update user profile with the form data
        current_user.profile.age = form.age.data
        current_user.profile.gender = form.gender.data
        current_user.profile.city = form.city.data
        current_user.profile.country = form.country.data
        current_user.profile.comfort_level = int(form.comfort_level.data)

        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form=form)


# TODO
# manage user locations 
@app.route('/manage_locations', methods = ['GET', 'POST'])
def manage_locations():
        return render_template('manage_locations.html',)


@app.route('/manage_wardrobe', methods=['GET', 'POST'])
@login_required
def manage_wardrobe():
    form = ManageWardrobeForm()

    if form.validate_on_submit():
        # Convert list of temperature ranges to comma-separated string
        temperature_ranges_str = ",".join(form.temperature_ranges.data) if form.temperature_ranges.data else ""

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


# delete a single wardrobe item
@app.route('/delete_wardrobe_item/<int:item_id>', methods=['POST'])
@login_required
def delete_wardrobe_item(item_id):
    item = UserClothingItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        return redirect(url_for('manage_wardrobe'))

    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('manage_wardrobe'))



@app.route('/register', methods = ['GET', 'POST'])
def register():
        form = RegistrationForm()
        if form.validate_on_submit():
                hashed_password = generate_password_hash(form.password.data)
                user = User(username = form.username.data, password = hashed_password)

                profile = Profile(
                        age = form.age.data, gender = form.gender.data,
                        city = form.city.data, country = form.country.data, 
                        comfort_level = int(form.comfort_level.data)
                )
                print(f"Adding user: {user.username} to the database.") # Debugging: user added
                db.session.add(user)
                db.session.commit()  # This commits both the user and profile to the database
                
                user.profile = profile
                db.session.add(profile)
                db.session.commit() # add user object in the database

                print(f"User {user.username} and profile saved to the database.") # Debugging: user and profiled saved

                login_user(user) # log the user in
                return redirect(url_for('home'))
        return render_template('register.html', form = form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
        
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

# weather api intergration
def get_weather(city_name):
        api_url = "http://api.weatherapi.com/v1/forecast.json"
        api_key = "7ea62c83afb24f108ea225710242211"
        days = 1

        # Make the API request
        response = requests.get(f"{api_url}?key={api_key}&q={city_name}&days={days}&aqi=no&alerts=yes")

        if response.status_code == 200:
                data = response.json()
        else:
                print("Error fetching weather data: ", response.status_code)

        current_weather = data.get("current", {})
        forecast_day = data.get("forecast", {}).get("forecastday", [])[0] if data.get("forecast") else {}

        for hour in forecast_day.get("hour", []):
                hour_time = hour.get("time")
                hour_condition = hour.get("condition", {}).get("text")
                hour_temp_c = hour.get("temp_c")
                hour_feels_like_c = hour.get("feelslike_c")
                hour_wind_speed_kph = hour.get("wind_kph")
                hour_precip_mm = hour.get("precip_mm")
                hour_visibility_km = hour.get("vis_km")
                hour_uv_index = hour.get("uv")
                hour_humidity = hour.get("humidity")
                
                
                # Store each hourly weather data entry in the database
                weather_entry = WeatherForecast(
                        city=city_name,
                        time=hour_time,
                        condition=hour_condition,
                        temperature=hour_temp_c,
                        feels_like=hour_feels_like_c,
                        wind_speed=hour_wind_speed_kph,
                        precipitation=hour_precip_mm,
                        uv_index=hour_uv_index,
                        visibility=hour_visibility_km,
                        humidity=hour_humidity
                )
                db.session.add(weather_entry)

        db.session.commit()  # Commit all the data

                 
        # Extract alert data
        # TODO: get customized alerts
        alerts = data.get("alerts", {}).get("alert", [])
        alert_headline = alerts[0].get("headline") if alerts else None

        

        return current_weather, alert_headline




if __name__ == "__main__":
        app.run(host="127.0.0.1", port=8080, debug=True)
