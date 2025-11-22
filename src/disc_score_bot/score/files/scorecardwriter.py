import csv
from pathlib import Path

class ScorecardWriter:
    """Scorecardwriter, can write scorecards to files"""
    def __init__(self, folder:Path, file_name:str):
        self.folder = folder
        self.file_name = file_name

    def write(self, header, data):
        """Write the csv file"""
        if not self.folder.exists():
            self.folder.mkdir()

        with open(f'{self.folder}/{self.file_name}', 'w', encoding='UTF8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(data)
