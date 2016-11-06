from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    balance = models.IntegerField(default=0)
    tasks_number = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_name(self):
        return self.user.username
