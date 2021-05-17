from django.contrib import admin
from .models import UserApproved, UserNotification

# Register your models here.

admin.site.register(UserApproved)
admin.site.register(UserNotification)