import csv
import datetime
from enum import Enum

from .udiscscorecardreader import UdiscScoreCardReader, udisc_scorecard_header
from .udisccompetitionreader import UdiscCompetitionReader, udisc_competition_header

class UdiscCsvTypes(Enum):
    UNKNOWN = 0
    SCORECARD = 1
    COMPETITION = 2

class UdiscCsvReader:
    def __init__(self, path="", file=""):
        self.path = path
        self.file = file
        self.type = self.identify_csv()

    def identify_csv(self):
        '''Identify the given csv input. Possible options is given in UdiscCsvTypes'''
        with open(f'{self.path}/{self.file}', encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            if udisc_scorecard_header[1] in reader.fieldnames and udisc_scorecard_header[2] in reader.fieldnames:
                return UdiscCsvTypes.SCORECARD
            if udisc_competition_header[0] in reader.fieldnames and udisc_competition_header[5] in reader.fieldnames:
                return UdiscCsvTypes.COMPETITION
        return UdiscCsvTypes.UNKNOWN

    def parse(self):
        '''Parse the given Scorecard, and return the correct Scorecard'''
        if self.type == UdiscCsvTypes.SCORECARD:
            reader = UdiscScoreCardReader(self.path, self.file)
            return reader.parse()
        if self.type == UdiscCsvTypes.COMPETITION:
            reader = UdiscCompetitionReader(self.path, self.file)
            return reader.parse()
        return None

    def contain_course(self, course):
        '''Parse the given dates, and return the Scorecard if it is a match'''
        if self.type == UdiscCsvTypes.SCORECARD:
            reader = UdiscScoreCardReader(self.path, self.file)
            return reader.contain_course(course)
        if self.type == UdiscCsvTypes.COMPETITION:
            reader = UdiscCompetitionReader(self.path, self.file)
            return reader.contain_course(course)
        return None

    def contain_dates(self, date:datetime, date_to:datetime):
        '''Parse the given dates, and return the Scorecard if it is a match'''
        if self.type == UdiscCsvTypes.SCORECARD:
            reader = UdiscScoreCardReader(self.path, self.file)
            return reader.contain_dates(date, date_to)
        if self.type == UdiscCsvTypes.COMPETITION:
            reader = UdiscCompetitionReader(self.path, self.file)
            return reader.contain_dates(date, date_to)
        return None


