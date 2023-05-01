from django.conf import settings
import requests

loc_api = "http://api.open-notify.org/iss-now.json"


def loc():
    req = requests.get(loc_api)
    if req.status_code == 200:

        data = req.json()['iss_position']
        print(data)
    else:
        return None


if __name__ == "__main__":
    print(loc())
