from datetime import datetime
import WeatherAPI


MAPPING = {"Clear": ["outdoors", "adventure", "tech", "parents", "family", "health", "wellness", "sports", "fitness", "education", "photography", "food", "writing", "language", "music", "movements", "lgbtq", "film", "games", "science", "beliefs", "art", "culture", "book", "reading", "dancing", "pets", "hobbies", "crafts", "fashion", "beauty", "social", "career", "business"], "Clouds": ["outdoors", "adventure", "tech", "parents", "family", "health", "wellness", "sports", "fitness", "education", "photography", "food", "writing", "language", "music", "movements", "lgbtq", "film", "games", "science", "beliefs", "art", "culture", "book", "reading", "dancing", "pets", "hobbies", "crafts", "fashion", "beauty", "social", "career", "business"], "Drizzle": ["tech", "parents", "family", "education", "photography", "food", "writing", "language", "music", "lgbtq", "film", "games", "science", "beliefs", "art", "culture", "book", "reading", "dancing", "hobbies", "crafts", "fashion", "beauty", "social", "career", "business"], "Rain": ["tech", "education", "food", "writing", "language", "music", "lgbtq", "film", "games", "science", "beliefs", "art", "culture", "book", "reading", "hobbies", "crafts", "fashion", "beauty", "social", "career", "business"], "Snow": ["tech", "education", "food", "writing", "language", "music", "lgbtq", "film", "games", "science", "beliefs", "art", "culture", "book", "reading", "hobbies", "crafts", "fashion", "beauty", "social", "career", "business"], "Atmosphere": ["tech", "education", "food", "writing", "language", "music", "lgbtq", "film", "games", "science", "beliefs", "art", "culture", "book", "reading", "hobbies", "crafts", "fashion", "beauty", "social", "career", "business"], "Thunderstorm": ["tech", "education", "food", "writing", "lgbtq", "film", "games", "science", "beliefs", "art", "culture", "book", "reading", "hobbies", "crafts", "fashion", "beauty", "career", "business"]}

def getWeatherFilterQuery(zipcode):
    weather = WeatherAPI.weatherApi()
    weather.get_place_weather_zipcode(str(zipcode))
    result_high, result_low = weather.get_average_tmperature()

    current_weather = {}
    current_weather['high_tempearture_daily'] = result_high
    current_weather['low_tempearture_daily'] = result_low
    current_weather['main_weather'] = main_weather = weather.get_main_weather()
    
    min_date = None
    for key in main_weather:
        d = datetime.strptime(key, '%Y-%m-%d')
        if not min_date:
            min_date = d
        else:
            min_date = min(d, min_date)
    min_date_key = min_date.strftime('%Y-%m-%d')
    recommendated_categories = MAPPING[main_weather[min_date_key]]
    query = ",".join(recommendated_categories)
    return current_weather, query