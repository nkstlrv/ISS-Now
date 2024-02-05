import requests

HUMANS_IN_SPACE_API = "http://api.open-notify.org/astros.json"


def people_iss():
    resp = [h['name'] for h in requests.get(HUMANS_IN_SPACE_API).json()['people'] if h['craft'] == 'ISS']

    data = {
        'number': len(resp),
        'people': resp
    }

    return data


if __name__ == "__main__":
    print(people_iss())
