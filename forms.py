from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, PasswordField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length

class UserProfileForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    city = StringField('Location(city)', validators=[DataRequired()])
    country = StringField('Location(country/region)', validators=[DataRequired()])
    comfort_level = SelectField('Comfort level (cooler to warmer)', choices=[
        (-2, 'Stay Much Cooler'),
        (-1, 'Stay Cooler'),
        (0, 'Neutral'),
        (1, 'Stay Warmer'),
        (2, 'Stay Much Warmer')
    ], default=0, validators=[DataRequired()])

    
    submit = SubmitField('Save Changes')


class RegistrationForm(FlaskForm):
    # User Creation
    username = StringField('Username', description = 'between 1 and 20 characters', 
                            validators=[DataRequired(), Length(min = 1, max = 20)])
    password = PasswordField('Password', description ='at least 6 characters', 
                            validators=[DataRequired(), Length(min = 6)])
    
    # Profile Creation
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    city = StringField('Location(city)', validators=[DataRequired()])
    country = StringField('Location(country/region)', validators=[DataRequired()])
    comfort_level = SelectField('Comfort level (cooler to warmer)', choices=[
        (-2, 'Stay Much Cooler'),
        (-1, 'Stay Cooler'),
        (0, 'Neutral'),
        (1, 'Stay Warmer'),
        (2, 'Stay Much Warmer')
    ], default=0, validators=[DataRequired()])

    
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    # User login
    username = StringField('Username', description = 'between 1 and 16 characters', 
                            validators=[DataRequired(), Length(min = 1, max = 16)])
    password = PasswordField('Password', description ='at least 6 characters', 
                            validators=[DataRequired(), Length(min = 6)])
    
    submit = SubmitField('Log In')

def str_to_bool(value):
    return value == 'True'

class ManageWardrobeForm(FlaskForm):
    name = StringField('Clothing Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('outerwear', 'Outerwear'),
        ('footwear', 'Footwear'),
        ('accessory', 'Accessory')
    ], validators=[DataRequired()])

    temperature_ranges = SelectMultipleField('Temperature Range', choices=[
        ('below_0', 'Below 0°C (Below 32°F)'),
        ('0_to_10', '0°C to 10°C (32°F to 50°F)'),
        ('10_to_20', '10°C to 20°C (50°F to 68°F)'),
        ('above_20', 'Above 20°C (Above 68°F)')
    ], option_widget=widgets.CheckboxInput(), coerce=str)

    precipitation_tag = SelectField('Suitable for Precipitation', choices=[('True', 'Yes'), ('False', 'No')], coerce=str_to_bool)
    wind_protection_tag = SelectField('Wind Protection', choices=[('True', 'Yes'), ('False', 'No')], coerce=str_to_bool)
    uv_protection_tag = SelectField('UV Protection', choices=[('True', 'Yes'), ('False', 'No')], coerce=str_to_bool)
    layer_type = SelectField('Layer Type', choices=[
        ('base', 'Base Layer'),
        ('mid', 'Mid Layer'),
        ('outer', 'Outer Layer')
    ], validators=[DataRequired()])
    setting = SelectField('Setting', choices=[
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('active', 'Active')
    ], validators=[DataRequired()])

    submit = SubmitField('Add Item')
