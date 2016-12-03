from django.contrib import admin
from .models import UserClar, AdminClar


class UserClarAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'title', 'text', 'is_read', 'time')
    search_fields = ('recipient__name', 'title', 'text')

admin.site.register(UserClar, UserClarAdmin)

admin.site.register(AdminClar)
