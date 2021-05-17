from django.contrib import admin
from .models import work, Personal, BankAccount, Experience, Education, PersonalImage

# Register your models here.

admin.site.register(work)
admin.site.register(Personal)
admin.site.register(BankAccount)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(PersonalImage)