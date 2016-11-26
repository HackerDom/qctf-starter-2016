from django.contrib import admin
from .models import Task, Hint, Flag, Submit

# Register your models here.
admin.site.register(Task)
admin.site.register(Hint)
admin.site.register(Flag)


class SubmitAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'task', 'flag', 'time')
    list_filter = ('task', 'team')
    search_fields = ('team__name', 'task__title', 'flag')

admin.site.register(Submit, SubmitAdmin)
