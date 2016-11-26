from django.db import models
from cabinet.models import Team


class UserClar(models.Model):
    recipient = models.ForeignKey(Team)
    title = models.CharField(max_length=100)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def mark_as_read(self):
        self.is_read = True
        self.save()

    class Meta:
        ordering = ['-time']


class AdminClar(models.Model):
    sender = models.ForeignKey(Team)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    is_read = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time']
