import datetime

class DiscgolfmetrixCompetition:
    def __init__(self, json):
        self.json = json
        self.competition_url = f'https://discgolfmetrix.com/{self.get_id()}'
        self.error = json.get("Errors")
        self.name = self.get_name()
        self.datetime = self.get_datetime()

    def __eq__(self, other):
        if self.datetime == other.datetime:
            return True

    def __lt__(self, other):
        if self.datetime < other.datetime:
            return True

    def __le__(self, other):
        if self.datetime <= other.datetime:
            return True

    def __gt__(self, other):
        if self.datetime < other.datetime:
            return True

    def __ge__(self, other):
        if self.datetime >= other.datetime:
            return True

    def get_name(self):
        if self.json is not None:
            competition = self.json.get("Competition")
            name = competition.get("Name")
            if not name:
                return None
            return name
        return None

    def get_id(self):
        if self.json is not None:
            competition = self.json.get("Competition")
            name = competition.get("ID")
            if not name:
                return None
            return name
        return None

    # "Date":"2017-06-02"
    # "Time":"09:34:00"
    def get_datetime(self):
        competition = self.json.get("Competition")
        date_time = datetime.datetime.strptime(f'{competition.get("Date")} {competition.get("Time")}','%Y-%m-%d %H:%M:%S')
        return date_time

    def is_valid(self):
        if self.error is None and self.name is not None:
            return True
        return False
