from os import getenv
import requests

class PdgaApi():
    """PDGA REST API - https://www.pdga.com/dev/api/rest/v1/auth

    Requires a PDGA developer account. Credentials are read from the
    ``PDGA_USERNAME`` and ``PDGA_PASSWORD`` environment variables unless
    supplied directly to :meth:`login`.
    """
    def __init__(self):
        self.name = 'pdga.com'
        self.url = 'https://www.pdga.com'
        self.api_url = 'https://api.pdga.com'
        self.sessid = None
        self.session_name = None
        self.token = None

    @property
    def is_authenticated(self):
        """True when a session has been established via :meth:`login`."""
        return bool(self.sessid and self.session_name)

    @property
    def cookie(self):
        """Session cookie header value (``session_name=sessid``)."""
        if not self.is_authenticated:
            return None
        return f'{self.session_name}={self.sessid}'

    def login(self, username=None, password=None):
        """Login - https://www.pdga.com/dev/api/rest/v1/auth
        Creates a new session for a given user and returns the session info.

        Endpoint: /services/json/user/login
        Method: POST

        Input parameters:
        1. username - defaults to the ``PDGA_USERNAME`` environment variable
        2. password - defaults to the ``PDGA_PASSWORD`` environment variable
        """
        username = username if username is not None else getenv("PDGA_USERNAME")
        password = password if password is not None else getenv("PDGA_PASSWORD")
        if not username or not password:
            return None

        data = {'username': username, 'password': password}
        response = requests.post(
            f'{self.api_url}/services/json/user/login',
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        if response and response.status_code == 200:
            body = response.json()
            self.sessid = body.get('sessid')
            self.session_name = body.get('session_name')
            self.token = body.get('token')
            return body
        return None

    def connect(self):
        """Connect - https://www.pdga.com/dev/api/rest/v1/auth
        Returns status for the current session.

        Endpoint: /services/json/system/connect
        Method: POST
        """
        if not self.is_authenticated:
            return None

        headers = {
            'X-CSRF-Token': self.token,
            'Cookie': self.cookie
        }
        response = requests.post(
            f'{self.api_url}/services/json/system/connect',
            headers=headers,
            timeout=10
        )
        if response and response.status_code == 200:
            return response.json()
        return None

    def logout(self):
        """Logout - https://www.pdga.com/dev/api/rest/v1/auth
        Destroys the session for the currently logged in user.

        Endpoint: /services/json/user/logout
        Method: POST
        """
        if not self.is_authenticated:
            return None

        headers = {
            'X-CSRF-Token': self.token,
            'Cookie': self.cookie
        }
        response = requests.post(
            f'{self.api_url}/services/json/user/logout',
            headers=headers,
            timeout=10
        )
        if response and response.status_code == 200:
            self.sessid = None
            self.session_name = None
            self.token = None
            return response.json()
        return None

    def _get(self, endpoint, params):
        """Perform an authenticated GET request and return the parsed JSON."""
        if not self.is_authenticated:
            return None

        params = {key: value for key, value in params.items() if value is not None}
        response = requests.get(
            f'{self.api_url}{endpoint}',
            params=params,
            headers={'Cookie': self.cookie},
            timeout=10
        )
        if response and response.status_code == 200:
            return response.json()
        return None

    def players(self, pdga_number=None, last_name=None, first_name=None, class_=None,
                city=None, state_prov=None, country=None, last_modified=None,
                limit=None, offset=None):
        """Player Search - https://www.pdga.com/dev/api/rest/v1/services#player-search
        Returns player data for all members current or expired. It does not
        return the player rating for members who are not current.

        Endpoint: /services/json/players
        Method: GET

        Input parameters:
        1. pdga_number
        2. last_name
        3. first_name
        4. class_ - P, A
        5. city
        6. state_prov - two to three character administrative area, region, state or province code
        7. country - two-letter country code
        8. last_modified - YYYY-MM-DD
        9. limit - default: 10; max: 200
        10. offset - default: 0
        """
        params = {
            'pdga_number': pdga_number,
            'last_name': last_name,
            'first_name': first_name,
            'class': class_,
            'city': city,
            'state_prov': state_prov,
            'country': country,
            'last_modified': last_modified,
            'limit': limit,
            'offset': offset
        }
        return self._get('/services/json/players', params)

    def player_statistics(self, year=None, class_=None, division_code=None, continent=None,
                          country=None, state_prov=None, gender=None, pdga_number=None,
                          last_modified=None, limit=None, offset=None):
        """Player Statistics - https://www.pdga.com/dev/api/rest/v1/services#player-statistics
        Returns player statistics for active members who were current and
        participated in one or more events in a given year.

        Endpoint: /services/json/player-statistics
        Method: GET

        Input parameters:
        1. year - YYYY
        2. class_ - P, A
        3. division_code - three to four character division code
        4. continent - two-letter continent code or 3 digit UN M49 code
        5. country - two-letter country code
        6. state_prov - two to three character administrative area, region, state or province code
        7. gender - M, F
        8. pdga_number
        9. last_modified - YYYY-MM-DD
        10. limit - default: 10; max: 200
        11. offset - default: 0
        """
        params = {
            'year': year,
            'class': class_,
            'division_code': division_code,
            'continent': continent,
            'country': country,
            'state_prov': state_prov,
            'gender': gender,
            'pdga_number': pdga_number,
            'last_modified': last_modified,
            'limit': limit,
            'offset': offset
        }
        return self._get('/services/json/player-statistics', params)

    def events(self, tournament_id=None, event_name=None, start_date=None, end_date=None,
               country=None, state=None, province=None, tier=None, classification=None,
               limit=None, offset=None):
        """Event Search - https://www.pdga.com/dev/api/rest/v1/services#event-search
        Returns events matching the requested parameters.

        Endpoint: /services/json/event
        Method: GET

        Input parameters:
        1. tournament_id
        2. event_name
        3. start_date - YYYY-MM-DD
        4. end_date - YYYY-MM-DD
        5. country - two letter country code
        6. state - two letter administrative area, region, state or province code
        7. province - two letter administrative area, region, state or province code
        8. tier - comma separated list of tier codes
        9. classification - Pro, Am, Pro-Am
        10. limit - default: 10; max: 200
        11. offset - default: 0
        """
        params = {
            'tournament_id': tournament_id,
            'event_name': event_name,
            'start_date': start_date,
            'end_date': end_date,
            'country': country,
            'state': state,
            'province': province,
            'tier': tier,
            'classification': classification,
            'limit': limit,
            'offset': offset
        }
        return self._get('/services/json/event', params)

    def courses(self, course_name=None, postal_code=None, city=None, country=None,
                state_prov=None, latitude=None, longitude=None, course_id=None,
                limit=None, offset=None):
        """Course Search - https://www.pdga.com/dev/api/rest/v1/services#course-search
        Returns courses matching the requested parameters.

        Endpoint: /services/json/course
        Method: GET

        Input parameters:
        1. course_name
        2. postal_code
        3. city
        4. country - two-letter country code
        5. state_prov - two to three character administrative area, region, state or province code
        6. latitude
        7. longitude
        8. course_id
        9. limit - default: 10; max: 200
        10. offset - default: 0
        """
        params = {
            'course_name': course_name,
            'postal_code': postal_code,
            'city': city,
            'country': country,
            'state_prov': state_prov,
            'latitude': latitude,
            'longitude': longitude,
            'course_id': course_id,
            'limit': limit,
            'offset': offset
        }
        return self._get('/services/json/course', params)
