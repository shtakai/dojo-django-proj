from django.contrib import admin
from django.contrib.auth.models import User
from .models import Member # import the models from the models.py file


admin.site.register(Member)
