# https://discgolfmetrix.com/?u=rule&ID=2

import html
import json
import requests


def metrix_logo():
    return 'https://discgolfmetrix.com/img/metrix_logo_for_facebook.png'

def metrix_favicon():
    return 'https://discgolfmetrix.com/assets/img/favicon.png'

class DiscgolfMetrixApi():
    def __init__(self):
        self.name = 'discgolfmetrix.com'
        self.url = 'https://discgolfmetrix.com'
        self.api_url = 'https://discgolfmetrix.com/api.php?'

    # Courses list - https://discgolfmetrix.com/?u=rule&ID=49
    # Return list of courses.
    # 1. country_code - required.check codes here https://datahub.io/core/country-list. Example url: https://discgolfmetrix.com/api.php?content=courses_list&country_code=EE
    # 2. name - optional. Example url: https://discgolfmetrix.com/api.php?content=courses_list&country_code=EE&name=a%
    def courses_list(self, country_code = "NO", course_name = None):
        params = dict()
        params["content"] = "courses_list"
        params["country_code"] = country_code
        if course_name is not None:
            params["name"] = course_name
        response = requests.get(self.api_url, params=params)
        if response and response.status_code == 200:
            return response.json()
        else:
            return None
    
    # Course - https://discgolfmetrix.com/?u=rule&ID=50
    # Get a course information. Example: https://discgolfmetrix.com/api.php?content=course&id=14800&code=XXX
    #
    # Input parameters:
    # 1. id - course identification
    # 2. code - personal integration code. You can found it in personal preferences at the end.   
    def course(self, course_id, code = None):
        params = dict()
        params["content"] = "course"
        params["id"] = course_id
        if code is not None:
            params["code"] = code
        response = requests.get(self.api_url, params = params)
        if response and response.status_code == 200:
            unescaped_text = html.unescape(response.text)
            return json.loads(unescaped_text)
        else:
            return None    

    # You can calculate rating by the formula:
    # Rating = (RatingValue2 - RatingValue1)*(Result - RatingResult1)/(RatingResult2 - RatingResult1)+RatingValue1
    def calucate_course_rating(self, rating_value_1, rating_value_2, rating_result_1, rating_result_2, result):
        return (rating_value_2 - rating_value_1)*(result - rating_result_1)/(rating_result_2 - rating_result_1)+rating_value_1

    # Results - https://discgolfmetrix.com/?u=rule&ID=38
    # Method: Get Results
    # Get Results method can be used to query results for a given competition. 
    # Competition in this context can be a single round, top level competition record with multiple rounds or even a series of competitions.
    def get_results(self, result_id):
        params = dict()
        params["content"] = "result"
        params["id"] = result_id
        response = requests.get(self.api_url, params=params)
        if response and response.status_code == 200 and response.json().get("Errors") is None:
            unescaped_text = html.unescape(response.text)
            return json.loads(unescaped_text)
        else:
            return None

    # Bagtag list - https://discgolfmetrix.com/?u=rule&ID=40
    def bagtag_list(self, bagtag_id):
        params = dict()
        params["content"] = "bagtag_list"
        params["id"] = bagtag_id
        response = requests.get(self.api_url, params=params)
        if response and response.status_code == 200:
            return response.json()
        else:
            return None

    # My competitions - https://discgolfmetrix.com/?u=rule&ID=60
    # Return list of my competitions
    # 1. code - take the code from your Settings Integration code
    def my_competitions(self, player_code):
        params = dict()
        params["content"] = "my_competitions"
        params["code"] = player_code
        response = requests.get(self.api_url, params=params)
        if response and response.status_code == 200:
            return response.json()
        else:
            return None