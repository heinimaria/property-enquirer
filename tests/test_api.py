import pytest
from source.propery_enquirer.api import PropertyEnquirer

test_enquirer = PropertyEnquirer("Southfields", 900000, 3)


def test_area_type():
    assert type(test_enquirer.area) is str


def test_price_type():
    assert type(test_enquirer.max_price) is int


def test_get_property_listings_result_count():
    actual_response = test_enquirer.get_property_listings()
    assert actual_response["result_count"] != 0


def test_get_property_listings_type():
    test_response = test_enquirer.get_property_listings()
    assert type(test_response) is dict


def test_fails_with_wrong_parameters():
    with pytest.raises(SystemExit):
        failed_enquirer = PropertyEnquirer("Earlsfield", "hello", 7)
        failed_enquirer.get_property_listings()


def test_fails_with_no_results():
    with pytest.raises(SystemExit):
        failed_enquirer = PropertyEnquirer("Earlsfield", 100000, 4)
        failed_enquirer.get_property_listings()




