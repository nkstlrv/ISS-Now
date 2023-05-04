import requests
import time

import requests
from django.core.mail import send_mail
from django.conf import settings

from calculations.unix_time_converter import unix_converter
from calculations.distance_geocoder import get_distance
from calculations.iss.iss_params import iss_data
from iss_app.models import Notify

loc_api = "http://api.open-notify.org/iss-now.json"


def loc():

    data = iss_data()
    iss_coordinates = (data['lat'], data['lon'])

    timestamp_now = int(time.time())

    try:
        users_to_notify = Notify.objects.filter(do_notify=True, last_notified__lt=(timestamp_now - 1800))
        print(f"Checked users to notify at {unix_converter(timestamp_now)}")

        if len(users_to_notify) > 0:

            for u in users_to_notify:
                try:
                    user_coordinates = (u.user.location.lat, u.user.location.lon)
                    dist = get_distance(user_coordinates, iss_coordinates)

                    if dist <= 600 and 'ecl' in data['vis']:

                        u.last_notified = timestamp_now
                        u.save()

                        send_mail(subject="ISS Flyover", recipient_list=[u.user.email],
                                  message=f"Hello there, {u.user.username}! 👋\n\n"
                                          f"Do not miss the International Space Station flyover 💫\n"
                                          f"It can be seen at your location now! 📍",
                                  from_email=settings.DEFAULT_FROM_EMAIL)

                        print(f"{u.user.username} notified at {unix_converter(timestamp_now)}")

                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)





if __name__ == "__main__":
    loc()
