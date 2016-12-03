from django.contrib import admin
from .models import Team, Region


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'tasks_number', 'stolen_flags')
    list_filter = ('region', 'stolen_flags')
    search_fields = ('name', 'region__title', 'region__name')

admin.site.register(Team, TeamAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'start_time')
    search_fields = ('name', 'title')

admin.site.register(Region, RegionAdmin)
