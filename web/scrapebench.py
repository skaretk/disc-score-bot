from concurrent.futures import ThreadPoolExecutor
import scraper

search = "firebird"
# Disc to test

class ScrapeBench():
    def __init__(self, search):
        self.search = search
        self.discs = []
        self.search_times = []        

    def test_scrape(self, print_discs):
        test_scraper = scraper.RocketDiscs(self.search)
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(test_scraper.scrape)

        print(f'Spent {test_scraper.search_time} scraping')
        self.search_times.append(test_scraper.search_time)

        self.discs.extend(test_scraper.discs)
        print(f'Found {len(self.discs)} disc(s) in stock!')
        if (print_discs == True):
            self.print_discs()

    def print_discs(self):
        for disc in self.discs:
            print(f'Disc:{disc.name}\nManufacturer:{disc.manufacturer}\nPrice: {disc.price}\n[{disc.store}]({disc.url})')

    def get_average_time(self):
        return sum(self.search_times) / len(self.search_times)

    def run_test(self):
      self.test_scrape(True)

    def run_loop_test(self, no_of_loops):
        for x in range(1, no_of_loops + 1):
            self.discs = []
            self.test_scrape(False)            
            print(f'loop {x} of {no_of_loops} [{x/no_of_loops*100}%]')
        print(f'Average Scraper time: {round(self.get_average_time(), 2)}s')
        print(f'Total time Scraping: {round(sum(self.search_times), 2)}s')        

workbench = ScrapeBench(search)
workbench.run_test()
# workbench.run_loop_test(10)
