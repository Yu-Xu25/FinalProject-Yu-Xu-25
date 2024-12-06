# FinalProject-Yu-Xu-25

# Weather Detector and Outfit Recommendation System 
## Here is what it can do: 
* User Profile Creation: Allow users to input demographic information (name, gender, age, etc.). Include comfort levels (stay warmer or cooler) that the user might like under the weather to tailor recommendations.
Weather Data Integration: Use API provided by *weather api* for reliable weather data. Fetch hourly weather forecasts to provide timely outfit recommendations throughout the day.
* Outfit Recommendations: Develop an algorithm that considers user preferences, current weather conditions (temperature, precipitation, wind), and their documented wardrobe(optional). Use a scoring system to rank clothing items based on warmth, weather resistance, and user preferences.
* Wardrobe Management: Allow users to input details of their clothing items into a database. Implement a tagging system (e.g., rainy, windy, temperature) to categorize clothing items for better recommendations.
* Location Management: Allow users to manage locations where they want to see recommendation of outfits.

## To-do list: 
example: 
* By the end of week 4, 
    * I will have researched user profile creation. 
    * I will have explored potential APIs for weather data. 
    * I will have explored web frameworks and made a basic web app that says “hello”.
* By the end of week 5, 
    * I will have a basic homepage, and 
    * I will have a basic user registration and login system to allow users to create profiles. 
    * I will have created a database model to store user profiles and preferences.
* By the end of week 6, 
    * I will have integerated the weather API to fetch current weather data based on user location. 
    * I will have basic weather information on the user's home page.
    * I will have developed the outfit recommendation algorithm considering weather conditions and user preferences.
* By the end of week 7, 
    * I will have created a sample wardrobe database to test outfit recommendations.
    * I will implement wardrobe management functionality, allowing users to input their clothing items.
    * Set up a tagging system for clothing items to categorize them (e.g., seasonal, weather type).
* By the end of week 8, 
    * I will have created a user-friendly, modulized and clean interface for displaying current weather, outfit recommendations, and wardrobe management.
    * I will have tested basic functionality for each module.
* Finally, 
    * I will have finalized the project by adding documentation, including API endpoints and usage instructions.
    * I will have prepared a presentation showcasing the project’s features and potential for future improvements.

Usage Instructions:
For visiting the website, go to link http://127.0.0.1:8080/ in your browser
To access the website in your terminal, download this repository. Direct to the path of this repo and enter command: *python main.py* . 
Hover your mouse on *Running on http://127.0.0.1:8080/*, press and hold the cmd key (for Mac) and click on the link. You should be directed to the website's home page.

 Future developments:
 * Travel Support: Enable users to input travel destinations and dates, and fetch weather forecasts according to the number of days for those locations. Provide packing lists or outfit suggestions based on the travel destination’s weather.
 * Layered Outfits: Recommend layered outfits for users against the colder weather, such that user can be more adaptable to temperature differences between indoors and outdoors.
 * Health Alerts: Alert of weather conditions that should be taken caution about for users with different health conditions. Inform users of optional outfit recommendations that can protect them from the weather.
 * use automatic tests to test the functionality of the web app.
