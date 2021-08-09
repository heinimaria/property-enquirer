from tabulate import tabulate
import pandas as pd
from pandas import DataFrame
import re

""" This class parses the api response, prints it on a boarrd and logs the data to files"""


class ListingParser:
    def __init__(self, response, area):
        self.response = response
        self.area = area

    """ Parse the API response and select the attributes we want to keep """
    def parse_listings(self) -> list:
        listings = self.response
        listings_list = []
        for listing in listings['listing']:
            listing_info = dict(listing_area=self.area,
                                listing_id=listing.get('listing_id', ''),
                                address=listing.get('displayable_address', ''),
                                num_bathrooms=listing.get('num_bathrooms', ''),
                                num_bedrooms=listing.get('num_bedrooms', ''),
                                price=listing.get('price', ''),
                                price_modifier=listing.get('price_modifier', ''),
                                price_change=listing.get('price_change', ''),
                                property_type=listing.get('property_type', ''),
                                image_url=listing.get('image_url', ''),
                                floor_plan=listing.get('floor_plan', ''),
                                short_description=listing.get('short_description'),
                                details_url=listing.get('details_url', ''),
                                agent_name=listing.get('agent_name', ''),
                                first_published_date=listing.get('first_published_date'),
                                last_published_date=listing.get('last_published_date'))

            listings_list.append(listing_info)

        return listings_list

    def property_listings(self) -> DataFrame:
        dataset = self.parse_listings()
        header = dataset[0].keys()
        rows = [x.values() for x in dataset]
        df = pd.DataFrame(rows, columns=header)
        new_df = self.clean_listings(df)
        return new_df

    """ Display the API response on a board """
    def property_listings_board(self) -> DataFrame:
        return tabulate(self.property_listings(), headers='keys', tablefmt='psql')

    @staticmethod
    def clean_listings(old_df) -> DataFrame:
        match = re.compile('<.*?>')
        old_df["short_description"] = old_df.short_description.str.replace(match, '')
        return old_df

    """ Log the API response to files """
    def file_listings(self) -> None:
        property_data = self.parse_listings()
        header = property_data[0].keys()
        rows = [x.values() for x in property_data]
        df = pd.DataFrame(rows, columns=header)
        clean_df = self.clean_listings(df)
        listing_area = clean_df["listing_area"][0]
        clean_df.to_csv("data/property_data/property_data_" + listing_area + ".csv", mode="w", index=False)
