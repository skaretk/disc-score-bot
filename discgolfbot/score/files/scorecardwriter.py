import csv
import os

class ScorecardWriter:
    """Scorecardwriter, can write scorecards to files"""
    def __init__(self, path, file):
        self.path = path
        self.file = file

    def write(self, header, data):
        """Write the csv file"""
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(f'{self.path}/{self.file}', 'w', encoding='UTF8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(data)
