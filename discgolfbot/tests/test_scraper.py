import context
from concurrent.futures import ThreadPoolExecutor
from scrapers import discsport
search = "firebird"
# Disc to test

class TestScraper():
    def __init__(self, search):
        self.search = search
        self.discs = []
        self.scraper_times = []

    def test_scrape(self, print_discs):
        test_scraper = discsport.DiscScraper(self.search)
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(test_scraper.scrape)
        
        self.scraper_times.append(test_scraper.scraper_time)

        self.discs.extend(test_scraper.discs)
        print(f'Found {len(self.discs)} disc(s) in stock!')
        if (print_discs == True):
            self.print_discs()

    def print_discs(self):
        for disc in self.discs:
            print(f'Disc:{disc.name}\nManufacturer:{disc.manufacturer}\nPrice: {disc.price}\n[{disc.store}]({disc.url})')

    def get_average_time(self):
        return sum(self.scraper_times) / len(self.scraper_times)

    def run_test(self):
      self.test_scrape(True)

    def run_loop_test(self, no_of_loops):
        for x in range(1, no_of_loops + 1):
            self.discs = []
            self.test_scrape(False)
            print(f'loop {x} of {no_of_loops} [{x/no_of_loops*100}%]')
        print(f'Average Scraper time: {round(self.get_average_time(), 2)}s')
        print(f'Total time Scraping: {round(sum(self.scraper_times), 2)}s')        

test = TestScraper(search)
#test.run_test()
test.run_loop_test(10)