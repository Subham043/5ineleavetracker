from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import date

# Create your models here.

class LeaveType(models.Model):
    PAID = 'PD'
    UNPAID = 'UD'
    ON_DUTY = 'OD'
    RESTRICTED_HOLIDAY = 'RH'
    DAYS = 'DY'
    HOURS = 'HR'
    LEAVE_TYPE_CHOICES = [
        (PAID, 'Paid'),
        (UNPAID, 'Unpaid'),
        (ON_DUTY, 'On Duty'),
        (RESTRICTED_HOLIDAY, 'Restricted Holiday'),
    ]
    UNITS_CHOICES = [
        (DAYS, 'Days'),
        (HOURS, 'Hours'),
    ]
    Name = models.CharField(max_length=50, blank=False, null=False)
    Code = models.CharField(max_length=50, blank=True, null=True)
    Leave_Type = models.CharField(
        max_length=2,
        choices=LEAVE_TYPE_CHOICES,
        default=UNPAID,
    )
    Unit = models.CharField(
        max_length=2,
        choices=UNITS_CHOICES,
        default=DAYS,
    )
    Description = models.TextField(default="", blank=True, null=True)
    Valid_From = models.DateField(auto_now=False, auto_now_add=False,  default=timezone.now)
    Valid_To = models.DateField(auto_now=False, auto_now_add=False,  default=timezone.now)
    Opening_Balance = models.CharField(max_length=50, blank=False, null=False)
    Maximum_Balance = models.CharField(max_length=50, blank=False, null=False)
    Holiday_Between_Leave_Period = models.CharField(max_length=50, blank=False, null=False, default="0")
    To_Be_Applied_Days_In_Advance = models.CharField(max_length=50, blank=False, null=False, default="0")
    Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed = models.CharField(max_length=50, blank=False, null=False, default="0")
    Minimum_Gap_Between_2_Application_In_Days = models.CharField(max_length=50, blank=False, null=False, default="0")
    


    def __str__(self):
        return self.Name

    def clean(self):
        if int(self.Opening_Balance) > int(self.Maximum_Balance):
            raise ValidationError('Maximum balance must be greater than Opening balance')



class ApplyLeave(models.Model):
    Employee = models.ForeignKey(User, on_delete=models.CASCADE)
    Leave_Type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True)
    Valid_From = models.DateField(auto_now=False, auto_now_add=False,  default=timezone.now)
    Valid_To = models.DateField(auto_now=False, auto_now_add=False,  default=timezone.now)
    Team_Email_ID = models.CharField(max_length=50, blank=True, null=True)
    Reason_For_Leave = models.TextField(default="", blank=True, null=True)
    Reason_For_Rejection = models.TextField(default="", blank=True, null=True)
    Approved = models.BooleanField(default=False)
    Rejected = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.Employee.username


    def clean(self):
        advanceDay = LeaveType.objects.get(id=self.Leave_Type.id)

        #Valid From date should be greater or equal to advanceDay
        today = date(datetime.today().year, datetime.today().month, datetime.today().day)
        given_day = date(self.Valid_From.year, self.Valid_From.month, self.Valid_From.day)
        diff = given_day - today
        if int(diff.days) < int(advanceDay.To_Be_Applied_Days_In_Advance):
            raise ValidationError(str(advanceDay) + ' should be applied '+ str(advanceDay.To_Be_Applied_Days_In_Advance) + ' days in advance')

        #Valid From date and Valid To date should not be  greater than advanceDay.Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed
        fromDate = date(self.Valid_From.year, self.Valid_From.month, self.Valid_From.day)
        toDate = date(self.Valid_To.year, self.Valid_To.month, self.Valid_To.day)
        diff = toDate - fromDate
        if int(diff.days) > int(advanceDay.Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed):
            raise ValidationError(str(advanceDay) + ' cannot exceed more than '+ str(advanceDay.Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed) + ' days')


        #Valid From date and Valid To date cannot be same
        if self.Valid_From == self.Valid_To:
            raise ValidationError('Valid From date and Valid To date cannot be same')

        

class LeaveAvailable(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leavetype = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    leaveAvailable = models.CharField(max_length=50, blank=True, null=True)
    leaveBooked = models.CharField(max_length=50, default='0')
    

    def __str__(self):
        return str(self.leavetype)

    def save(self, *args, **kwargs):
        self.leaveAvailable = self.leavetype.Opening_Balance
        super(LeaveAvailable, self).save(*args, **kwargs)

    @receiver(post_save, sender=LeaveType)
    def create_LeaveAvailable(sender, instance, created, **kwargs):
        if created:
            user = User.objects.all()
            for i in user:
                LeaveAvailable.objects.create(employee=i,leavetype=instance)
            

    @receiver(post_save, sender=get_user_model())
    def create_LeaveAvailable_user(sender, instance, created, **kwargs):
        if created:
            user = LeaveType.objects.all()
            for i in user:
                LeaveAvailable.objects.create(employee=instance,leavetype=i)

    

class HolidayList(models.Model):
    EVENT = 'EVENT'
    HOLIDAY = 'HOLIDAY'
    TYPE_CHOICES = [
        (EVENT, 'Event'),
        (HOLIDAY, 'Holiday'),
    ]
    Name = models.CharField(max_length=50, blank=False, null=False)
    Date = models.DateField(auto_now=False, auto_now_add=False,  default=timezone.now)
    Description = models.TextField(default="", blank=True, null=True)
    Type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default=HOLIDAY,
    )
    EveryYear = models.BooleanField(default=False)

    def __str__(self):
        return str(self.Name)

    
