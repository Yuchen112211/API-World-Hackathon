from datetime import datetime
import WeatherAPI


MAPPING = {"Clear": ["Outdoors & Adventure", "Tech", "Family", "Health & Wellness", "Sports & Fitness", "Learning", "Photography", "Food & Drink", "Writing", "Language & Culture", "Music", "Movements", "LGBTQ", "Film", "Sci-Fi & Games", "Beliefs", "Arts", "Book Clubs", "Dance", "Pets", "Hobbies & Crafts", "Fashion & Beauty", "Social", "Career & Business"], "Clouds": ["Outdoors & Adventure", "Tech", "Family", "Health & Wellness", "Sports & Fitness", "Learning", "Photography", "Food & Drink", "Writing", "Language & Culture", "Music", "Movements", "LGBTQ", "Film", "Sci-Fi & Games", "Beliefs", "Arts", "Book Clubs", "Dance", "Pets", "Hobbies & Crafts", "Fashion & Beauty", "Social", "Career & Business"], "Drizzle": ["Tech", "Family", "Learning", "Photography", "Food & Drink", "Writing", "Language & Culture", "Music", "LGBTQ", "Film", "Sci-Fi & Games", "Beliefs", "Arts", "Book Clubs", "Dance", "Hobbies & Crafts", "Fashion & Beauty", "Social", "Career & Business"], "Rain": ["Tech", "Learning", "Food & Drink", "Writing", "Language & Culture", "Music", "LGBTQ", "Film", "Sci-Fi & Games", "Beliefs", "Arts", "Book Clubs", "Hobbies & Crafts", "Fashion & Beauty", "Social", "Career & Business"], "Snow": ["Tech", "Learning", "Food & Drink", "Writing", "Language & Culture", "Music", "LGBTQ", "Film", "Sci-Fi & Games", "Beliefs", "Arts", "Book Clubs", "Hobbies & Crafts", "Fashion & Beauty", "Social", "Career & Business"], "Atmosphere": ["Tech", "Learning", "Food & Drink", "Writing", "Language & Culture", "Music", "LGBTQ", "Film", "Sci-Fi & Games", "Beliefs", "Arts", "Book Clubs", "Hobbies & Crafts", "Fashion & Beauty", "Social", "Career & Business"], "Thunderstorm": ["Tech", "Learning", "Food & Drink", "Writing", "LGBTQ", "Film", "Sci-Fi & Games", "Beliefs", "Arts", "Book Clubs", "Hobbies & Crafts", "Fashion & Beauty", "Career & Business"]}

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