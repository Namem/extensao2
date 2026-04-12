from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tenant

admin.site.register(Tenant)
admin.site.register(CustomUser, UserAdmin)