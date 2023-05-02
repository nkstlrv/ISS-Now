from django.conf import settings
import requests
from geopy.geocoders import Nominatim
from geopy import distance
from iss_app.models import Location

loc_api = "http://api.open-notify.org/iss-now.json"


def loc():
    req = requests.get(loc_api)
    if req.status_code == 200:

        l = Location.objects.all()
        print(l)

        data = req.json()['iss_position']
        print(data)
    else:
        return None


if __name__ == "__main__":
    loc()
