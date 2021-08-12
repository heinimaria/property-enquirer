from source.propery_enquirer.api import PropertyEnquirer
from property_listings import ListingParser


def run() -> None:
    areas = ["Southfields", "Earlsfield", "Putney", "Wandsworth"]
    for a in areas:
        property_enquiry = PropertyEnquirer(a)
        api_response = property_enquiry.get_property_listings()

        listing = ListingParser(api_response, property_enquiry.area)
        listing.property_listings_board()


if __name__ == '__main__':
    run()

