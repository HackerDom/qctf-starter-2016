from __future__ import unicode_literals
from django.db import models
from cabinet.models import Team


class Task(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    flag = models.CharField(max_length=64)

    def __str__(self):
        return self.title

    def _is_submited(self, team):
        return Submit.objects.filter(team=team, task=self,
                                     is_correct=True).exists()

    def _award_team(self, team):
        team.tasks_number += 1
        team.balance += self.price
        team.save()

    def submit_flag(self, team, flag):
        status = self.flag == flag
        if not self._is_submited(team) and status:
            self._award_team(team)
            submit = Submit(team=team, task=self, is_correct=True)
            submit.save()
        return status


class Submit(models.Model):
    team = models.ForeignKey(Team)
    task = models.ForeignKey(Task)
    is_correct = models.BooleanField(default=False)
