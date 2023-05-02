from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='location')
    city = models.CharField(blank=False, null=False, max_length=200)
    country = models.CharField(blank=False, null=False, max_length=200)

    def __str__(self):
        return f"{self.user.username} | {self.city} | {self.country}"



