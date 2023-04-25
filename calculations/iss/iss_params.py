import requests
from calculations import unix_time_converter

ISS_API = "https://api.wheretheiss.at/v1/satellites/25544"


def iss_data():
    req = requests.get(ISS_API).json()

    iss_daytime = {
        'value': None
    }

    if req['visibility'] == 'daylight':
        iss_daytime['value'] = 'Day ☀️'
    elif req['visibility'] == 'eclipsed':
        iss_daytime['value'] = 'Night 🌛'
    else:
        iss_daytime['value'] = 'No Data'


    data = {

        'lat': req["latitude"],
        'lon': req["longitude"],
        'alt': req["altitude"],
        'vel_kph': int(req["velocity"]),
        'vel_mps': round((int(req["velocity"]) / 3.6), 2),
        'vis': req['visibility'],
        'day_night': iss_daytime['value']

    }

    return data


if __name__ == "__main__":
    print()
    print(iss_data())
