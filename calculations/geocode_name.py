import requests
import os
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

load_dotenv()


def check_if_exist(city_name):
    geolocator = Nominatim(user_agent="ISS_NOW")
    location = geolocator.geocode(city_name)
    return location


if __name__ == "__main__":
    print(check_if_exist('borispil'))