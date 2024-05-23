import html
import json
import requests

def metrix_logo():
    """Get the metrix logo"""
    return 'https://discgolfmetrix.com/img/metrix_logo_for_facebook.png'

def metrix_favicon():
    """Get the metrix favicon"""
    return 'https://discgolfmetrix.com/assets/img/favicon.png'

class DiscgolfMetrixApi():
    """Discgolfmetric API - https://discgolfmetrix.com/?u=rule&ID=37"""
    def __init__(self):
        self.name = 'discgolfmetrix.com'
        self.url = 'https://discgolfmetrix.com'
        self.api_url = 'https://discgolfmetrix.com/api.php?'

    def courses_list(self, country_code="NO", course_name=None):
        """Return list of courses. - https://discgolfmetrix.com/?u=rule&ID=49

        Input parameters:
        1. country_code - required.check codes here https://datahub.io/core/country-list. Example url: https://discgolfmetrix.com/api.php?content=courses_list&country_code=EE
        2. name - optional. Example url: https://discgolfmetrix.com/api.php?content=courses_list&country_code=EE&name=a%
        """
        params = {
            'content': 'courses_list',
            'country_code': country_code
        }
        if course_name is not None:
            params["name"] = f'{course_name}%'
        response = requests.get(self.api_url, params=params, timeout=10)
        if response and response.status_code == 200:
            return json.loads(html.unescape(response.text))
        return None

    def course(self, course_id, code=None):
        """Course - https://discgolfmetrix.com/?u=rule&ID=50
        Get a course information. Example: https://discgolfmetrix.com/api.php?content=course&id=14800&code=XXX

        Input parameters:
        1. id - course identification
        2. code - personal integration code. You can found it in personal preferences at the end.
        """
        params = {
            'content': 'course',
            'id': course_id
        }
        if code is not None:
            params["code"] = code
        response = requests.get(self.api_url, params=params, timeout=10)
        if response and response.status_code == 200:
            return json.loads(html.unescape(response.text))
        return None

    def calucate_course_rating(self, rating_value_1, rating_value_2, rating_result_1, rating_result_2, result):
        """Calculate Rating
        Rating = (RatingValue2 - RatingValue1)*(Result - RatingResult1)/(RatingResult2 - RatingResult1)+RatingValue1

        Input parameters:
        1. rating_value_1
        2. rating_value_2
        3. rating_result_1
        4. rating_result_2
        5. result
        """
        return (rating_value_2 - rating_value_1)*(result - rating_result_1)/(rating_result_2 - rating_result_1)+rating_value_1

    def get_results(self, result_id, class_=None, group=None):
        """Get Results from Competitions - https://discgolfmetrix.com/?u=rule&ID=38
        Get Results method can be used to query results for a given competition.
        Competition in this context can be a single round, top level competition record with multiple rounds or even a series of competitions.

        Input parameters:
        1. result_id*: Competition ID
        """
        params = {
            'content': 'result',
            'id': result_id
        }
        if class_ is not None:
            params['class'] = class_
        if group is not None:
            params['group'] = group
        response = requests.get(self.api_url, params=params, timeout=10)
        if response and response.status_code == 200 and bool(response.json().get("Errors")) is False:
            return json.loads(html.unescape(response.text))
        return None

    def bagtag_list(self, bagtag_id):
        """Bagtag list - https://discgolfmetrix.com/?u=rule&ID=40

        Input parameters:
        1. content: always 'bagtag_list'
        2. id: bagtag list identificator.
        """
        params = {
            'content': 'bagtag_list',
            'id': bagtag_id
        }
        response = requests.get(self.api_url, params=params, timeout=10)
        if response and response.status_code == 200:
            return response.json()
        return None

    # My competitions - https://discgolfmetrix.com/?u=rule&ID=60
    # Return list of my competitions
    # 1. code - take the code from your Settings Integration code
    def my_competitions(self, code):
        """My competitions - https://discgolfmetrix.com/?u=rule&ID=60
        Return list of my competitions

        Input parameters:
        1. code: take the code from your Settings Integration code
        """
        params = {
            'content': 'my_competitions',
            'code': code
        }
        response = requests.get(self.api_url, params=params, timeout=10)
        if response and response.status_code == 200:
            return response.json()
        return None