from django.contrib import admin
from .models import Task, Hint, Flag

# Register your models here.
admin.site.register(Task)
admin.site.register(Hint)
admin.site.register(Flag)
