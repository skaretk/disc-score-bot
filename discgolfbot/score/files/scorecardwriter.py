import csv
import os

class ScorecardWriter:
    def __init__(self, path, file):
        self.path = path
        self.file = file
    
    def write(self, header, data):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            
        with open(f'{self.path}/{self.file}', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)
