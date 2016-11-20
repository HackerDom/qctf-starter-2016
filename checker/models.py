from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.conf import settings
from cabinet.models import Team


class Task(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.PositiveIntegerField()
    flag = models.CharField(max_length=64)
    teams = models.ManyToManyField(Team, related_name='tasks', blank=True)

    result_message = models.TextField()

    def __str__(self):
        return self.title

    def _award_team(self, team):
        team.tasks_number += 1
        team.balance += self.price
        team.save()

    def is_solved(self, team):
        return self.teams.filter(pk=team.pk).exists()

    def _check_delay(self, team):
        time = timezone.now() - settings.SUBMIT_DELAY
        return not Submit.objects.filter(team=team, time__gt=time).exists()

    def submit_flag(self, team, flag):
        if not self._check_delay(team):
            return 'Please wait.'

        correct = self.flag == flag
        status = 'ok' if correct else 'Wrong flag.'
        submit = Submit(team=team, flag=flag)
        submit.save()
        if not self.is_solved(team) and correct:
            self._award_team(team)
            self.teams.add(team)
        # check time
        return status


class Hint(models.Model):
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    text = models.TextField()
    owners = models.ManyToManyField(Team, related_name='hints', blank=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.name

    def is_bought(self, team):
        return self.owners.filter(pk=team.pk).exists()

    def buy(self, team):
        if not self.is_bought(team) and team.balance >= self.price:
            self.owners.add(team)
            team.spend_money(self.price)

    def get_hint_text(self, team):
        return self.text if self.is_bought(team) else ''


class Submit(models.Model):
    team = models.ForeignKey(Team)
    flag = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
