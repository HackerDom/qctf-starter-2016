from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings


class Team(models.Model):
    balance = models.PositiveIntegerField(default=0)
    tasks_number = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    replace_info = models.TextField(blank=True, default='[]')
    start_time = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.user.username

    def get_name(self):
        return self.user.username

    def spend_money(self, number):
        self.balance -= number
        self.save()

    def get_place(self):
        teams = Team.objects.filter(tasks_number__gt=self.tasks_number).count()
        return teams + 1

    def contest_started(self):
        return timezone.now() >= self.start_time

    def contest_finished(self):
        return timezone.now() > self.start_time + settings.CONTEST_DURATION


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Team.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.team.save()
