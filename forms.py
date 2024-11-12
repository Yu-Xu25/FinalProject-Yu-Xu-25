from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

# TODO: for edit use
class UserProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    city = StringField('Location(city)', validators=[DataRequired()])
    country = StringField('Location(country/region)', validators=[DataRequired()])
    sense_temp = SelectField('Sensitivity to temperature (optional)', choices=[
        ('NA', 'NA'),
        ('Not Sensitive', 'Not Sensitive'),
        ('Less Sensitive', 'Less Sensitive'),
        ('Average Sensitive', 'Average Sensitive'),
        ('More Sensitive', 'More Sensitive'),
        ('Most Sensitive', 'Most Sensitive')
    ])
    sense_light = SelectField('Sensitivity to lightness (optional)', choices=[
        ('NA', 'NA'),
        ('Not Sensitive', 'Not Sensitive'),
        ('Less Sensitive', 'Less Sensitive'),
        ('Average Sensitive', 'Average Sensitive'),
        ('More Sensitive', 'More Sensitive'),
        ('Most Sensitive', 'Most Sensitive')
    ])
    sense_humid = SelectField('Sensitivity to humidity (optional)', choices=[
        ('NA', 'NA'),
        ('Not Sensitive', 'Not Sensitive'),
        ('Less Sensitive', 'Less Sensitive'),
        ('Average Sensitive', 'Average Sensitive'),
        ('More Sensitive', 'More Sensitive'),
        ('Most Sensitive', 'Most Sensitive')
    ])
    allegies = SelectField('Have Allegies (optional)', choices=[('NA', 'NA'), ('Yes', 'Yes'), ('No', 'No')])
    asthma = SelectField('Have Asthma (optional)', choices=[('NA', 'NA'), ('Yes', 'Yes'), ('No', 'No')])
    other = StringField('Other health conditions? (optional)')
    submit = SubmitField('Sumbit')


class RegistrationForm(FlaskForm):
    username = StringField('Username', description = 'between 1 and 20 characters', 
                            validators=[DataRequired(), Length(min = 1, max = 20)])
    password = PasswordField('Password', description ='at least 6 characters', 
                            validators=[DataRequired(), Length(min = 6)])
    
    # Profile Creation
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    city = StringField('Location(city)', validators=[DataRequired()])
    country = StringField('Location(country/region)', validators=[DataRequired()])
    sense_temp = SelectField('Sensitivity to temperature (optional)', choices=[
        ('NA', 'NA'),
        ('Not Sensitive', 'Not Sensitive'),
        ('Less Sensitive', 'Less Sensitive'),
        ('Average Sensitive', 'Average Sensitive'),
        ('More Sensitive', 'More Sensitive'),
        ('Most Sensitive', 'Most Sensitive')
    ])
    sense_light = SelectField('Sensitivity to lightness (optional)', choices=[
        ('NA', 'NA'),
        ('Not Sensitive', 'Not Sensitive'),
        ('Less Sensitive', 'Less Sensitive'),
        ('Average Sensitive', 'Average Sensitive'),
        ('More Sensitive', 'More Sensitive'),
        ('Most Sensitive', 'Most Sensitive')
    ])
    sense_humid = SelectField('Sensitivity to humidity (optional)', choices=[
        ('NA', 'NA'),
        ('Not Sensitive', 'Not Sensitive'),
        ('Less Sensitive', 'Less Sensitive'),
        ('Average Sensitive', 'Average Sensitive'),
        ('More Sensitive', 'More Sensitive'),
        ('Most Sensitive', 'Most Sensitive')
    ])
    allegies = SelectField('Have Allegies (optional)', choices=[('NA', 'NA'), ('Yes', 'Yes'), ('No', 'No')])
    asthma = SelectField('Have Asthma (optional)', choices=[('NA', 'NA'), ('Yes', 'Yes'), ('No', 'No')])
    other = StringField('Other health conditions? (optional)')

    
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    username = StringField('Username', description = 'between 1 and 16 characters', 
                            validators=[DataRequired(), Length(min = 1, max = 16)])
    password = PasswordField('Password', description ='at least 6 characters', 
                            validators=[DataRequired(), Length(min = 6)])
    
    submit = SubmitField('Log in')