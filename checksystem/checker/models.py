from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from cabinet.models import Team


class Task(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.PositiveIntegerField()
    teams = models.ManyToManyField(Team, related_name='tasks', blank=True)

    parent = models.ForeignKey('self', blank=True, null=True,
                               related_name='children')
    default_flag = models.CharField(blank=True, default='', max_length=100)

    correct_flag_message = models.TextField()
    wrong_flag_message = models.TextField()

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.title

    def _award_team(self, team):
        team.sumbit_time = timezone.now() - team.get_start_time()
        team.tasks_number += 1
        team.balance += self.price
        team.save()

    def _get_flag(self, team):
        flag = Flag.objects.filter(team=team, task=self).first()
        if flag is None:
            return self.default_flag if self.default_flag else None
        return flag.flag

    def is_solved(self, team):
        return self.teams.filter(pk=team.pk).exists()

    def _check_delay(self, team):
        time = timezone.now() - settings.SUBMIT_DELAY
        return not Submit.objects.filter(team=team, time__gt=time).exists()

    @transaction.atomic
    def submit_flag(self, team, flag):
        need_refresh = False
        if not self._check_delay(team):
            return {'message': 'Please wait.', 'is_correct': False}
        if team.contest_finished():
            return {'message': 'Contest is alreay finished.',
                    'is_correct': False}
        if not team.contest_started():
            return {'message': 'Contest is not started.', 'is_correct': False}
        correct_flag = self._get_flag(team)
        if correct_flag is None:
            return {'message': 'No flag for you. :(', 'is_correct': False}

        is_correct = correct_flag.lower() == flag.lower()
        message = self.correct_flag_message if is_correct else \
            self.wrong_flag_message

        submit = Submit(team=team, flag=flag)
        submit.save()

        if not self.is_solved(team) and is_correct:
            if self.children.count() > 0:
                need_refresh = True
            self._award_team(team)
            self.teams.add(team)

        return {'message': message, 'is_correct': is_correct,
                'need_refresh': need_refresh}


class Hint(models.Model):
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    price = models.PositiveIntegerField()
    text = models.TextField()
    owners = models.ManyToManyField(Team, related_name='hints', blank=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.name

    def is_bought(self, team):
        return self.owners.filter(pk=team.pk).exists()

    @transaction.atomic
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


class Flag(models.Model):
    team = models.ForeignKey(Team)
    task = models.ForeignKey(Task)
    flag = models.CharField(max_length=100)

    def __str__(self):
        return "{}'s {} flag".format(self.team.user.username, self.task.title)
