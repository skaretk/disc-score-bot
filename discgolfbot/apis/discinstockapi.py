import requests

class DiscinstockApi():
    def __init__(self):
        self.name = 'discinstock.no'
        self.url = 'https://discinstock.no/'
        self.api_url = 'https://api.discinstock.no'

    # Discs - https://api.discinstock.no/discs
    # Return list of discs
    def discs(self):
        params = dict()
        params["in_stock"] = "true"
        params["limit"] = "9999"
        params["skip"] = "0"
        response = requests.get(self.api_url + '/discs' , params=params)
        if response and response.status_code == 200:
            return response.json()
        else:
            return None

    # Discs search - https://api.discinstock.no/discs/search
    # Return list of discs from a retailer
    def discs_search(self, spider_name):
        params = dict()
        params["spider_name"] = spider_name
        response = requests.get(self.api_url + '/discs/search' , params=params)
        if response and response.status_code == 200:
            return response.json()
        else:
            return None
    
    # Brands - https://api.discinstock.no/discs/brands
    # Return list of brands
    def brands(self):
        response = requests.get(self.api_url + '/brands')
        if response and response.status_code == 200:
            return response.json()
        else:
            return None
    
    # List retailers - https://api.discinstock.no/retailers
    # Return list of retailers
    def retailers(self):
        response = requests.get(self.api_url + '/retailers')
        if response and response.status_code == 200:
            return response.json()
        else:
            return None
