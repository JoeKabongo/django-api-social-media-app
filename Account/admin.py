from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, UpdatePasswordToken

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'isWriter')

admin.site.register(UserAccount, UserAdmin)
admin.site.register(UpdatePasswordToken)
