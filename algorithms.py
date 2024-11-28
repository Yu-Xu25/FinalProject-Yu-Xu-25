def calculate_heat_index(temp_f, humidity):
    # Constants for the Heat Index formula
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = -42.38, 2.049, 10.14, -0.2248, -0.006838, -0.05482, 0.001228, 0.0008528, -0.00000199
    HI = (c1 + c2 * temp_f + c3 * humidity + c4 * temp_f * humidity + 
          c5 * temp_f**2 + c6 * humidity**2 + c7 * temp_f**2 * humidity + 
          c8 * temp_f * humidity**2 + c9 * temp_f**2 * humidity**2)
    return HI

def calculate_wind_chill(temp_f, wind_speed_mph):
    # Wind Chill formula
    Twc = 35.74 + 0.6215 * temp_f - 35.75 * wind_speed_mph**0.16 + 0.4275 * temp_f * wind_speed_mph**0.16
    return Twc

# calculate apparent temperature customized for a given user given their profile entry 
# reference: https://www.meteor.iastate.edu/~ckarsten/bufkit/apparent_temperature.html
def calculate_apparent_temperature(weather_data):
    
    temp_c = weather_data.get('temp_c', 0)
    wind_speed_kph = weather_data.get('wind_kph', 0)
    humidity = weather_data.get('humidity', 0)

    temp_f = (temp_c * 9/5) + 32  # Convert Celsius to Fahrenheit
    wind_speed_mph = wind_speed_kph * 0.62 # Convert kph to mph for wind chill formula

    # Calculate Heat Index (if applicable, for temperatures above 80°F)
    if temp_f > 80:
        heat_index = calculate_heat_index(temp_f, humidity)
        apparent_temp = heat_index
    # Calculate Wind Chill (if applicable, for temperatures below 50°F)
    elif temp_f < 50:
        wind_chill = calculate_wind_chill(temp_f, wind_speed_mph)  
        apparent_temp = wind_chill
    else:
        apparent_temp = temp_f  # Between 50°F and 80°F, use the actual temperature (ambient air temperature)


    return apparent_temp


# TODO
# get default outfit recommendations based on current weather data
def get_default_outfit_recommendations(weather_data, sample_items):
    pass
        

# TODO
# get outfit recommendations for an user based on current weather data as well as their profile entry
def get_outfit_recommendations(weather_data, comfort_level, clothing_items):
    pass
    


