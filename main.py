# render HTML templates, redirecting user to another page through url
from flask import Flask, render_template, redirect, url_for
# provide user session management, adds useful methods for user management (like is_authenticated, is_active, get_id())
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# allow interact with the database using Python classes instead of writing SQL queries
from flask_sqlalchemy import SQLAlchemy
# allow hashing passwords for security
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import secrets

from forms import UserProfileForm, RegistrationForm, LoginForm
from models import db, User, Profile


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
        return render_template('home.html')

# create a db table based on models
@app.before_request
def create_tables():
        db.drop_all()
        db.create_all()

# profile creation 
@app.route('/profile', methods = ['GET', 'POST'])
def profile():
        user_profile = current_user.profile
        return render_template('profile.html', profile = user_profile)

@app.route('/register', methods = ['GET', 'POST'])
def register():
        form = RegistrationForm()
        if form.validate_on_submit():
                hashed_password = generate_password_hash(form.password.data)
                user = User(username = form.username.data, password = hashed_password)

                profile = Profile(
                        age = form.age.data, gender = form.gender.data,
                        city = form.city.data, country = form.country.data, 
                        sense_temp = form.sense_temp.data, sense_light = form.sense_light.data,
                        sense_humidity = form.sense_humid.data, has_allegies = form.allegies.data,
                        has_asthma = form.asthma.data, other = form.other.data
                )
                
                db.session.add(user)
                db.session.add(profile)
                # db.session.commit() # add user object in the database

                user.profile = profile
                db.session.commit()

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
                # TODO: LOGIN FAILED! FIGURE OUT WHY
                if user and check_password_hash(user.password, form.password.data):
                        login_user(user)
                        return redirect(url_for('home'))
        return render_template('login.html', form = form)

# weather api intergration
@app.route('/weather', methods=['GET'])
def weather():
        pass


if __name__ == "__main__":
        app.run(host="127.0.0.1", port=8080, debug=True)
