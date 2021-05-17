from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from leave.models import ApplyLeave

# Create your models here.

class UserApproved(models.Model):
    Employee = models.OneToOneField(User, on_delete=models.CASCADE)
    AdminApproved = models.BooleanField(default=False)

    def __str__(self):
        return self.Employee.username

class UserNotification(models.Model):
    Employee = models.OneToOneField(User, on_delete=models.CASCADE)
    NewEmployee = models.BooleanField(default=False)
    NewLeave = models.BooleanField(default=False)
    LeaveStatus = models.BooleanField(default=False)

    def __str__(self):
        return self.Employee.username

    @receiver(post_save, sender=get_user_model())
    def create_UserNotification(sender, instance, created, **kwargs):
        if created:
            user = User.objects.filter(is_superuser=True)
            for i in user:
                try:
                    notif = UserNotification.objects.get(Employee=i)
                    notif.NewEmployee = True
                    notif.save()
                except:
                    pass


    @receiver(post_save, sender=ApplyLeave)
    def create_UserNotification_leave(sender, instance, created, **kwargs):
        if created:
            user = User.objects.filter(is_superuser=True)
            for i in user:
                try:
                    notif = UserNotification.objects.get(Employee=i)
                    notif.NewLeave = True
                    notif.save()
                except:
                    pass
