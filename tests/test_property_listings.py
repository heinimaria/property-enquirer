import pytest
from pandas.util.testing import assert_frame_equal
import pandas as pd

from source.propery_enquirer.property_listings import ListingParser
from source.propery_enquirer.api import PropertyEnquirer


@pytest.fixture()
def test_board():
    test_data = [{'listing_area': 'Southfields',
                  'listing_id': '58026214',
                  'address': 'Cowdrey Road, Wimbledon SW19',
                  'num_bathrooms': '1',
                  'num_bedrooms': '3',
                  'price': '800000',
                  'price_modifier': 'guide_price',
                  'price_change': [{'direction': '', 'date': '2021-03-18 18:00:45', 'percent': '0%', 'price': 830000},
                                   {'direction': 'down', 'date': '2021-04-20 17:01:08', 'percent': '-3.6%',
                                    'price': 800000}],
                  'property_type': '',
                  'image_url': 'https://lid.zoocdn.com/354/255/60acd62c456b57066eada76c602ceb015bcf59c4.jpg',
                  'floor_plan': ['https://lc.zoocdn.com/9388f8d34e138d6104261598c6677ac81d0b03c7.jpg'],
                  'short_description': 'This well presented three bedroom end of terrace period family home is conveniently located just a short walk from Haydons road station with its regular services into London via Thames link and Wimbledon town centre with its wide range of shops, bars and restaurants and Wimbledon station with its regular services into London as well as access to the District line. The accommodation on offer comprises of two separate receptions, a good size kitchen/diner and on the first floor are three double bedrooms and the family bathroom. Outside is a well maintained private rear garden. For further information please contact Lauristons estate agents in Wimbledon on .',
                  'details_url': 'https://www.zoopla.co.uk/for-sale/details/58026214?utm_source=v1:9KyNAjLUAErIr0e_fqJyoGH9KgVohKCX&utm_medium=api',
                  'agent_name': 'Lauristons - Wimbledon',
                  'first_published_date': '2021-03-18 22:03:49',
                  'last_published_date': '2021-08-08 21:06:02'},
                 {'listing_area': 'Southfields',
                  'listing_id': '59028079',
                  'address': 'Balvernie Grove, Southfields, London SW18',
                  'num_bathrooms': 1,
                  'num_bedrooms': 3,
                  'price': '800000',
                  'price_modifier': '',
                  'price_change': [{'direction': '', 'date': '2021-06-28 18:23:29', 'percent': '0%', 'price': '899950'},
                                   {'direction': 'down', 'date': '2021-07-07 08:24:44', 'percent': '-5.5%',
                                    'price': '850000'},
                                   {'direction': 'down', 'date': '2021-08-06 09:57:13', 'percent': '-5.8%',
                                    'price': '800000'}],
                  'property_type': 'Terraced house',
                  'image_url': 'https://lid.zoocdn.com/354/255/a1f977cd7f8a4124091a9ab394e41c8cf530e54e.jpg',
                  'floor_plan': ['https://lc.zoocdn.com/1d080e37681c3f117c9672f59f6d2e1d5c706300.jpg'],
                  'short_description': "Offered to the market with no onward chain this wonderful three double bedroom house is well positioned on Balvernie Grove only moments away from the 'Outstanding' Sheringdale Primary School and Southfields Village/ Tube.",
                  'details_url': 'https://www.zoopla.co.uk/for-sale/details/59028079?utm_source=v1:9KyNAjLUAErIr0e_fqJyoGH9KgVohKCX&utm_medium=api',
                  'agent_name': 'Barnard Marcus - Southfields', 'first_published_date': '2021-06-28 18:24:47',
                  'last_published_date': '2021-08-09 10:33:31'}]
    return test_data


test_querier = PropertyEnquirer("Southfields", 900000, 3)
response = test_querier.get_property_listings()
listing_parser = ListingParser(response, "Southfields")


def test_parse_listings_response_type():
    assert type(listing_parser.parse_listings()) is list


def test_parse_listings_response_not_empty():
    assert listing_parser.parse_listings() != ""


def test_parse_listings_response_keys():
    expected_keys = ['listing_area', 'listing_id', 'address', 'num_bathrooms', 'num_bedrooms', 'price', 'price_modifier',
                     'price_change', 'property_type', 'image_url', 'floor_plan', 'short_description', 'details_url',
                     'agent_name', 'first_published_date', 'last_published_date']
    actual_keys = list(listing_parser.parse_listings()[0].keys())
    assert actual_keys == expected_keys


def test_clean_listings():
    input_data = [['<p>heini</p>', 30], ['<p>skye</p>', 1], ['<p>jamie</p>', 30]]
    columns = ["short_description", "age"]
    input_df = pd.DataFrame(input_data, columns=columns)
    expected = [['heini', 30], ['skye', 1], ['jamie', 30]]
    expected_df = pd.DataFrame(expected, columns=columns)
    assert_frame_equal(listing_parser.clean_listings(input_df), expected_df)


def test_property_listings_not_empty():
    assert listing_parser.property_listings() is not None


def test_property_listings_number_columns():
    assert len(listing_parser.property_listings().columns) == 16


def test_property_listings_columns():
    expected_headers = ['listing_area', 'listing_id', 'address', 'num_bathrooms', 'num_bedrooms', 'price',
                        'price_modifier', 'price_change', 'property_type', 'image_url', 'floor_plan',
                        'short_description', 'details_url', 'agent_name', 'first_published_date', 'last_published_date']
    actual_headers = listing_parser.property_listings().columns.values.tolist()
    assert actual_headers == expected_headers


def test_property_listings_board_not_empty():
    assert listing_parser.property_listings_board() != ""
