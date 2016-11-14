from django.contrib import admin
from .models import Task, Hint

# Register your models here.
admin.site.register(Task)
admin.site.register(Hint)
