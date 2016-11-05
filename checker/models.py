from __future__ import unicode_literals

from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    flag = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Submit(models.Model):
    # team
    task = models.ForeignKey(Task)
    is_correct = models.BooleanField(default=False)
