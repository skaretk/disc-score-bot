import time
from concurrent.futures import ThreadPoolExecutor
import scraper

# Get scrape info:
disc_search = "compass"

class ScrapeBench():
  def __init__(self, search):
    self.search = search
    self.discs = []
  
  def testScrape(self):
      test_scraper = scraper.Latitude64(self.search)

      start_time = time.time()

      with ThreadPoolExecutor(max_workers=7) as executor:
          future = executor.submit(test_scraper.scrape)

      end_time = time.time()
      print(f'Spent {end_time - start_time} scraping')

      self.discs.extend(test_scraper.discs)
      print(f'Found {len(self.discs)} disc(s) in stock!')
      
      
  def printDiscs(self):
      for disc in self.discs:            
          print(f'Disc:{disc.name} Manufacturer:{disc.manufacturer} Price: {disc.price} [{disc.store}]({disc.url})')


# Run test scrape
workbench = ScrapeBench(disc_search)
workbench.testScrape()
workbench.printDiscs()
