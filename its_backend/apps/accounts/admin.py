# accounts/admin.py
from django.contrib import admin

from .models import CustomUser, Teaches

admin.site.register(CustomUser)
admin.site.register(Teaches)
