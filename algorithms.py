from models import *
import random


# get default outfit recommendations based on current weather data
def get_default_outfit_recommendations(weather_data):
    feels_like_temp = weather_data['feelslike_c']

    # Determine which temperature range the feels-like temperature falls into
    if feels_like_temp < 0:
        temp_range = "below_0"
    elif 0 <= feels_like_temp <= 10:
        temp_range = "0_to_10"
    elif 10 < feels_like_temp <= 20:
        temp_range = "10_to_20"
    else:
        temp_range = "above_20"

    # Query items that include the relevant temperature range
    wardrobe_items = SampleClothingItem.query.all()
    suitable_items = [item for item in wardrobe_items if temp_range in item.temperature_ranges.split(",")]

    # Core outfit recommendations based on feels-like temperature
    outfit = {
        "top": choose_item(suitable_items, category="top"),
        "bottom": choose_item(suitable_items, category="bottom"),
        "footwear": choose_item(suitable_items, category="footwear"),
        "outerwear": choose_item(suitable_items, category="outerwear", optional=(feels_like_temp > 15))
    }

    # Optional outfit considerations for wind, precipitation, and UV
    optional_outfit = {
        "precipitation": choose_item(suitable_items, tag="precipitation_tag") \
            if weather_data['precip_mm'] > 0 else None,
        "wind_protection": choose_item(suitable_items, tag="wind_protection_tag") \
            if weather_data['wind_kph'] > 15 else None,
        "uv_protection": choose_item(suitable_items, tag="uv_protection_tag") \
            if weather_data['uv'] > 5 else None
    }

    # Messages for optional items
    messages = []
    if weather_data['precip_mm'] > 0 or weather_data['wind_kph'] > 15 or weather_data['uv'] > 5:
        if weather_data['precip_mm'] > 0 and optional_outfit['precipitation'] is None:
            messages.append("You might want to get prepared for this rainy day!")
        if weather_data['wind_kph'] > 15 and optional_outfit['wind_protection'] is None:
            messages.append("You might want to get prepared for this windy day!")
        if weather_data['uv'] > 5 and optional_outfit['uv_protection'] is None:
            messages.append("You might want to protect yourself from the sun!")
    else:
        messages.append("Enjoy this wonderful weather!")

    return {
        "outfit": outfit,
        "optional_outfit": optional_outfit,
        "messages": messages
    }
        

# get outfit recommendations for an user based on current weather data as well as their profile entry
def get_outfit_recommendations(weather_data, user_profile):
    feels_like_temp = weather_data['feelslike_c'] + (user_profile.comfort_level * 5)

    # Determine which temperature range the feels-like temperature falls into
    if feels_like_temp < 0:
        temp_range = "below_0"
    elif 0 <= feels_like_temp <= 10:
        temp_range = "0_to_10"
    elif 10 < feels_like_temp <= 20:
        temp_range = "10_to_20"
    else:
        temp_range = "above_20"

    # Query items that include the relevant temperature range
    wardrobe_items = UserClothingItem.query.filter(UserClothingItem.user_id == user_profile.user_id).all()
    suitable_items = [item for item in wardrobe_items if temp_range in item.temperature_ranges.split(",")]

    # Core outfit recommendations based on feels-like temperature
    outfit = {
        "top": choose_item(suitable_items, category="top"),
        "bottom": choose_item(suitable_items, category="bottom"),
        "footwear": choose_item(suitable_items, category="footwear"),
        "outerwear": choose_item(suitable_items, category="outerwear", optional=(feels_like_temp > 15))
    }

    # Optional outfit considerations for wind, precipitation, and UV
    optional_outfit = {
        "precipitation": choose_item(suitable_items, tag="precipitation_tag") \
            if weather_data['precip_mm'] > 0 else None,
        "wind_protection": choose_item(suitable_items, tag="wind_protection_tag") \
            if weather_data['wind_kph'] > 15 else None,
        "uv_protection": choose_item(suitable_items, tag="uv_protection_tag") \
            if weather_data['uv'] > 5 else None
    }

    # Messages for optional items
    messages = []
    if weather_data['precip_mm'] > 0 or weather_data['wind_kph'] > 15 or weather_data['uv'] > 5:
        if weather_data['precip_mm'] > 0 and optional_outfit['precipitation'] is None:
            messages.append("You might want to get prepared for this rainy day!")
        if weather_data['wind_kph'] > 15 and optional_outfit['wind_protection'] is None:
            messages.append("You might want to get prepared for this windy day!")
        if weather_data['uv'] > 5 and optional_outfit['uv_protection'] is None:
            messages.append("You might want to protect yourself from the sun!")
    else:
        messages.append("Enjoy this wonderful weather!")
    
    return {
        "outfit": outfit,
        "optional_outfit": optional_outfit,
        "messages": messages
    }


# Selects an item from the given list based on the specified category, and optionally a tag.
def choose_item(items, category=None, tag=None, optional=False):
    # tag (str): Optional; tag to filter the items further (e.g., 'precipitation_tag').
    # optional (bool): If True, returns None if no item is found.

    if category:
        items = [item for item in items if item.category == category]

    if tag:
        items = [item for item in items if getattr(item, tag, False)]

    # If no items are found and the item is optional, return None
    if optional and not items:
        return None

    # Return the first item if available, otherwise None
    return random.choice(items) if items else None


# Function to populate sample data for a newly registered user
def populate_user_wardrobe(user_id):
    sample_items = SampleClothingItem.query.all()
    for item in sample_items:
        user_item = UserClothingItem(
            name=item.name,
            category=item.category,
            temperature_ranges=item.temperature_ranges,
            precipitation_tag=item.precipitation_tag,
            wind_protection_tag=item.wind_protection_tag,
            uv_protection_tag=item.uv_protection_tag,
            layer_type=item.layer_type,
            setting=item.setting,
            user_id=user_id
        )
        db.session.add(user_item)
    db.session.commit()



# Add around 10 clothing items that cover a variety of conditions 
# in the SampleClothingItem
def populate_sample_data():
    sample_items = [
        SampleClothingItem(
            name="Puffer Jacket",
            category="outerwear",
            temperature_ranges="below_0,0_to_10",
            precipitation_tag=True,
            wind_protection_tag=True,
            uv_protection_tag=False,
            layer_type="outer",
            setting="casual"
        ),
        SampleClothingItem(
            name="Raincoat",
            category="outerwear",
            temperature_ranges="0_to_10,10_to_20",
            precipitation_tag=True,
            wind_protection_tag=False,
            uv_protection_tag=False,
            layer_type="outer",
            setting="active"
        ),
        SampleClothingItem(
            name="T-Shirt",
            category="top",
            temperature_ranges="10_to_20,above_20",
            precipitation_tag=False,
            wind_protection_tag=False,
            uv_protection_tag=False,
            layer_type="base",
            setting="casual"
        ),
        SampleClothingItem(
            name="Sunglasses",
            category="accessory",
            temperature_ranges="above_20",
            precipitation_tag=False,
            wind_protection_tag=False,
            uv_protection_tag=True,
            layer_type=None,
            setting="casual"
        ),
        SampleClothingItem(
            name="Windbreaker Jacket",
            category="outerwear",
            temperature_ranges="10_to_20,above_20",
            precipitation_tag=False,
            wind_protection_tag=True,
            uv_protection_tag=False,
            layer_type="outer",
            setting="active"
        ),
        SampleClothingItem(
            name="Jeans",
            category="bottom",
            temperature_ranges="0_to_10,10_to_20,above_20",
            precipitation_tag=False,
            wind_protection_tag=False,
            uv_protection_tag=False,
            layer_type="mid",
            setting="casual"
        ),
        SampleClothingItem(
            name="Wool Sweater",
            category="top",
            temperature_ranges="below_0,0_to_10",
            precipitation_tag=False,
            wind_protection_tag=False,
            uv_protection_tag=False,
            layer_type="mid",
            setting="formal"
        ),
        SampleClothingItem(
            name="Running Shoes",
            category="footwear",
            temperature_ranges="0_to_10,10_to_20,above_20",
            precipitation_tag=False,
            wind_protection_tag=False,
            uv_protection_tag=False,
            layer_type=None,
            setting="active"
        ),
        SampleClothingItem(
            name="Baseball Cap",
            category="accessory",
            temperature_ranges="10_to_20,above_20",
            precipitation_tag=False,
            wind_protection_tag=False,
            uv_protection_tag=True,
            layer_type=None,
            setting="casual"
        ),
        SampleClothingItem(
            name="Thermal Leggings",
            category="bottom",
            temperature_ranges="below_0,0_to_10",
            precipitation_tag=False,
            wind_protection_tag=True,
            uv_protection_tag=False,
            layer_type="base",
            setting="active"
        )
    ]

    # Populate SampleClothingItem table if empty
    if not SampleClothingItem.query.first():
        for item in sample_items:
            db.session.add(item)
        db.session.commit()
