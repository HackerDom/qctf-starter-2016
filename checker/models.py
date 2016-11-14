from __future__ import unicode_literals
from django.db import models
from cabinet.models import Team


class Task(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.PositiveIntegerField()
    flag = models.CharField(max_length=64)
    teams = models.ManyToManyField(Team, related_name='tasks', blank=True)

    def __str__(self):
        return self.title

    def _is_submited(self, team):
        return self.teams.filter(pk=team.pk).exists()

    def _award_team(self, team):
        team.tasks_number += 1
        team.balance += self.price
        team.save()

    def submit_flag(self, team, flag):
        status = self.flag == flag
        if not self._is_submited(team) and status:
            self._award_team(team)
            self.teams.add(team)
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
