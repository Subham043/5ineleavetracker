from django.contrib import admin
from .models import LeaveType, ApplyLeave, LeaveAvailable, HolidayList

# Register your models here.
admin.site.register(LeaveType)
admin.site.register(ApplyLeave)
admin.site.register(LeaveAvailable)
admin.site.register(HolidayList)