from django.contrib import admin
from .models import Task, Hint, Flag, Submit


class HintAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'name', 'description', 'price')
    search_fields = ('task__title', 'name', 'description')

admin.site.register(Hint, HintAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price', 'default_flag')
    search_fields = ('title', 'description', 'default_flag')

admin.site.register(Task, TaskAdmin)


class FlagAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'task', 'flag')
    list_filter = (('task', admin.RelatedOnlyFieldListFilter), 'team')
    search_fields = ('team__name', 'task__title', 'flag')

admin.site.register(Flag, FlagAdmin)


class SubmitAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'task', 'flag', 'time')
    list_filter = (('task', admin.RelatedOnlyFieldListFilter), 'team')
    search_fields = ('team__name', 'task__title', 'flag')

admin.site.register(Submit, SubmitAdmin)
