from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(blank=False, null=False, max_length=200)
    country = models.CharField(blank=False, null=False, max_length=200)

    def __str__(self):
        return f"{self.user.username} | {self.city | self.country}"