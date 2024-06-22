import csv
import datetime
from pathlib import Path
from .udisc_scorecard_reader import UdiscScoreCardReader, udisc_scorecard_header, udisc_scorecard_header_old
from .udisc_competition_reader import UdiscCompetitionReader, udisc_competition_header
from .udisc_csv_types import UdiscCsvTypes

class UdiscCsvReader:
    """uDisc csv reader, can identify and read the correct type of csv files"""
    def __init__(self, file:Path):
        self.file = file
        self.type = self.identify_csv()

    def identify_csv(self):
        """Identify the given csv input. Possible options is given in UdiscCsvTypes"""
        with open(self.file, encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            if udisc_scorecard_header[7] in reader.fieldnames: # Cotain RoundRating - new csv
                return UdiscCsvTypes.SCORECARD
            if udisc_scorecard_header_old[1] in reader.fieldnames and udisc_scorecard_header_old[2] in reader.fieldnames:
                return UdiscCsvTypes.SCORECARD_OLD
            if udisc_competition_header[0] in reader.fieldnames and udisc_competition_header[5] in reader.fieldnames:
                return UdiscCsvTypes.COMPETITION
        return UdiscCsvTypes.UNKNOWN

    def parse(self):
        """Parse the given Scorecard, and return the correct Scorecard"""
        if self.type in {UdiscCsvTypes.SCORECARD_OLD, UdiscCsvTypes.SCORECARD}:
            reader = UdiscScoreCardReader(self.file, self.type)
            return reader.parse()
        if self.type == UdiscCsvTypes.COMPETITION:
            reader = UdiscCompetitionReader(self.file)
            return reader.parse()
        return None

    def contain_course(self, course):
        """Parse the given dates, and return the Scorecard if it is a match"""
        if self.type in {UdiscCsvTypes.SCORECARD_OLD, UdiscCsvTypes.SCORECARD}:
            reader = UdiscScoreCardReader(self.file, self.type)
            return reader.contain_course(course)
        if self.type == UdiscCsvTypes.COMPETITION:
            reader = UdiscCompetitionReader(self.file)
            return reader.contain_course(course)
        return None

    def contain_dates(self, date:datetime, date_to:datetime):
        """Parse the given dates, and return the Scorecard if it is a match"""
        if self.type in {UdiscCsvTypes.SCORECARD_OLD, UdiscCsvTypes.SCORECARD}:
            reader = UdiscScoreCardReader(self.file, self.type)
            return reader.contain_dates(date, date_to)
        if self.type == UdiscCsvTypes.COMPETITION:
            reader = UdiscCompetitionReader(self.file)
            return reader.contain_dates(date, date_to)
        return None
