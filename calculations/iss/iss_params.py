import requests
from calculations import unix_time_converter


ISS_API = "https://api.wheretheiss.at/v1/satellites/25544"


def iss_data():
    req = requests.get(ISS_API).json()
    data = {

        'lat': req["latitude"],
        'lon': req["longitude"],
        'alt': req["altitude"],
        'vel_kph': int(req["velocity"]),
        'vel_mps': round((int(req["velocity"])/3.6), 2),
        'vis': req["visibility"],
        'daynum': req["daynum"],
    }

    return data


if __name__ == "__main__":

    print(iss_data())