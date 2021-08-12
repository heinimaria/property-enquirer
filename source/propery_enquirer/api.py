import os
import requests
from dotenv import load_dotenv
import json

""" 
The PropertyEnquirer class takes a few parameters and calls the Zoopla API. 
API_TOKEN is saved as an environmental variable.      
"""


class PropertyEnquirer:
    load_dotenv()

    def __init__(self, area: str, max_price=800000, min_beds=3):
        self.area = area
        self.max_price = max_price
        self.min_beds = min_beds
        self.token = os.environ.get("API_TOKEN")
        self.api = "http://api.zoopla.co.uk/api/v1/property_listings.json?listing_status=sale&property_type=houses&" \
                   "area=" + self.area + "&" + "maximum_price=" + str(self.max_price) + "&" + "minimum_beds=" + \
                   str(self.min_beds) + "&" + "page_size=100&" + "api_key=" + self.token

    """ Returns the API response as json """
    def get_property_listings(self) -> json:
        response = requests.get(self.api)
        json_response = response.json()
        try:
            if json_response["result_count"] == 0:
                raise Exception("No results found, change the search criteria. Quitting program...")
            else:
                return json_response
        except KeyError:
            raise Exception("Invalid input parameters, quitting program...")
