import time
from concurrent.futures import ThreadPoolExecutor
import scraper

# Get scrape info:
search = "firebird"

class ScrapeBench():
  def __init__(self, search):
    self.search = search
    self.discs = []
  
  def testScrape(self):
      test_scraper = scraper.RocketDiscs(self.search)

      start_time = time.time()

      with ThreadPoolExecutor(max_workers=1) as executor:
          future = executor.submit(test_scraper.scrape)

      end_time = time.time()
      print(f'Spent {end_time - start_time} scraping')

      self.discs.extend(test_scraper.discs)
      print(f'Found {len(self.discs)} disc(s) in stock!')
      
      
  def printDiscs(self):
      for disc in self.discs:            
          print(f'Disc:{disc.name}\nManufacturer:{disc.manufacturer}\nPrice: {disc.price}\n[{disc.store}]({disc.url})')


# Run test scrape
workbench = ScrapeBench(search)
workbench.testScrape()
workbench.printDiscs()
