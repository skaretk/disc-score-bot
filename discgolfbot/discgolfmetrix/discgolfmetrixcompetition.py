import datetime

class DiscgolfmetrixCompetition:
    """Discgolfmetrix Competition"""
    def __init__(self, json):
        self.json = json
        self.competition_url = f'https://discgolfmetrix.com/{self.get_id()}'
        self.error = json.get("Errors")
        self.name = self.get_name()
        self.datetime = self.get_datetime()

    def __eq__(self, other):
         return self.datetime == other.datetime

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __le__(self, other):
        return self.datetime <= other.datetime

    def __gt__(self, other):
        return self.datetime < other.datetime

    def __ge__(self, other):
        return self.datetime >= other.datetime

    def get_name(self):
        """Discgolfmetrix competition name"""
        if self.json is not None:
            competition = self.json.get("Competition")
            name = competition.get("Name")
            if not name:
                return None
            return name
        return None

    def get_id(self):
        """Discgolfmetrix competition ID"""
        if self.json is not None:
            competition = self.json.get("Competition")
            name = competition.get("ID")
            if not name:
                return None
            return name
        return None

    def get_datetime(self):
        """Return datetime for competition
        "Date":"2017-06-02"
        "Time":"09:34:00"
        """
        competition = self.json.get("Competition")
        date_time = datetime.datetime.strptime(f'{competition.get("Date")} {competition.get("Time")}','%Y-%m-%d %H:%M:%S')
        return date_time

    def is_valid(self):
        """Is the competition valid"""
        if self.error is None and self.name is not None:
            return True
        return False
