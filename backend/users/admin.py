from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Añade aquí cualquier configuración adicional

admin.site.register(CustomUser, CustomUserAdmin)