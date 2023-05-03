from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='location')
    city = models.CharField(blank=False, null=False, max_length=200)
    country = models.CharField(blank=False, null=False, max_length=200)
    lat = models.FloatField(default=None, null=True)
    lon = models.FloatField(default=None, null=True)

    def __str__(self):
        return f"{self.user.username} | {self.city} | {self.country}"


class Notify(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notify')
    do_notify = models.BooleanField(default=True)
    last_notified = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"{self.user.username} | {self.do_notify}"
