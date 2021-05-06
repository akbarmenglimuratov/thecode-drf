from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {
        	'fields': ('verified', 'date_of_birth', 'reputation')
        }),
    )

admin.site.register(models.User, CustomUserAdmin)	
