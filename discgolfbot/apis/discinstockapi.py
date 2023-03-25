import requests

class DiscinstockApi():
    """Discinstock api class - https://api.discinstock.no/docs"""
    def __init__(self):
        self.name = 'discinstock.no'
        self.url = 'https://discinstock.no/'
        self.api_url = 'https://api.discinstock.no'

    def discs(self):
        """Discs - Return list of discs - https://api.discinstock.no/discs"""
        params = {
            'in_stock': 'True',
            'limit': '9999',
            'skip': '0'
            }
        response = requests.get(f'{self.api_url}/discs', params=params, timeout=10)
        if response and response.status_code == 200:
            return response.json()
        return None

    def discs_search(self, spider_name):
        """Discs Search - Return list of discs from a retailer - https://api.discinstock.no/discs/search"""
        params = {'spider_name': spider_name}
        response = requests.get(f'{self.api_url}/discs/search', params=params, timeout=10)
        if response and response.status_code == 200:
            return response.json()
        return None

    def brands(self):
        """Brands - Return lists of brands - https://api.discinstock.no/discs/brands"""
        response = requests.get(f'{self.api_url}/brands', timeout=10)
        if response and response.status_code == 200:
            return response.json()
        return None

    def retailers(self):
        """Retailers - Return list of retailers - https://api.discinstock.no/retailers"""
        response = requests.get(f'{self.api_url}/retailers', timeout=10)
        if response and response.status_code == 200:
            return response.json()
        return None
