import requests


class PeopleISS:
    HUMANS_IN_SPACE_API = "http://api.open-notify.org/astros.json"

    def people_iss(self):
        resp = [h['name'] for h in requests.get(self.HUMANS_IN_SPACE_API).json()['people'] if h['craft'] == 'ISS']

        data = {
            'number': len(resp),
            'people': resp
        }

        return data


if __name__ == "__main__":
    p = PeopleISS()
    print(p.people_iss())
