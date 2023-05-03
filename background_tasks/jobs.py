from django.conf import settings
import requests
import time

from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
from geopy import distance
from iss_app.models import Location, Notify
from calculations.unix_time_converter import unix_converter
from django.core.mail import send_mail
from django.conf import settings


loc_api = "http://api.open-notify.org/iss-now.json"


def loc():
    req = requests.get(loc_api)

    timestamp_now = int(time.time())
    print(f"Checked users to notify at {unix_converter(timestamp_now)}")

    if req.status_code == 200:

        try:
            users_to_notify = Notify.objects.filter(do_notify=True, last_notified__lt=(timestamp_now-10))
            users_to_notify_test = User.objects.filter(location)

            for u in users_to_notify:
                u.last_notified = timestamp_now
                u.save()

                send_mail(subject="Flyover", recipient_list=[u.user.email], message="Test Message",
                          from_email=settings.DEFAULT_FROM_EMAIL)
                print(f"{u.user.username} notified at {unix_converter(timestamp_now)}")

        except Exception as e:
            print("No users to notify \n", e)

    else:
        return None


if __name__ == "__main__":
    loc()
