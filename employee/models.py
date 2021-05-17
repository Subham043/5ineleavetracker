from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from department.models import department
from designation.models import designation
from roles.models import roles
import datetime
from UserAuth.models import UserApproved
from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class work(models.Model):
    ACTIVE = 'AV'
    TERMINATED = 'TM'
    DECEASED = 'DS'
    RESIGNED = 'RN'
    PERMANENT = 'PM'
    ON_CONTRACT = 'OC'
    TEMPORARY = 'TP'
    TRAINEE = 'TR'
    EMPLOYEE_STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (TERMINATED, 'Terminated'),
        (DECEASED, 'Deceased'),
        (RESIGNED, 'Resigned'),
    ]
    EMPLOYEE_TYPE_CHOICES = [
        (PERMANENT, 'Permanent'),
        (ON_CONTRACT, 'On Contract'),
        (TEMPORARY, 'Temporary'),
        (TRAINEE, 'Trainee'),
    ]
    Employee = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user',)
    Department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True, related_name='department',)
    Reporting_To = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reporting',)
    Source_Of_Hire = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='source',)
    Location = models.CharField(max_length=50, blank=True, null=True)
    Title = models.ForeignKey(designation, on_delete=models.SET_NULL, null=True, related_name='job_title',)
    Date_Of_Joining = models.DateField(auto_now=False, auto_now_add=False,  default=timezone.now)
    Employee_Status = models.CharField(
        max_length=2,
        choices=EMPLOYEE_STATUS_CHOICES,
        default=ACTIVE,
    )
    Employee_Type = models.CharField(
        max_length=2,
        choices=EMPLOYEE_TYPE_CHOICES,
        default=TRAINEE,
    )
    Work_Phone = models.CharField(max_length=50, blank=True, null=True)
    Extension = models.CharField(max_length=50, blank=True, null=True)
    Role = models.ForeignKey(roles, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.Employee.username


class Personal(models.Model):
    SINGLE = 'SG'
    MARRIED = 'MD'
    MALE = 'ML'
    FEMALE = 'FL'
    MARITAL_STATUS_CHOICES = [
        (SINGLE, 'Single'),
        (MARRIED, 'Married'),
    ]
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    Employee = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='employee',)
    Mobile_Phone = models.CharField(max_length=50, blank=True, null=True)
    Other_Email = models.CharField(max_length=50, blank=True, null=True)
    Address = models.TextField(blank=True, null=True)
    Date_Of_Birth = models.DateField(auto_now=False, auto_now_add=False,  default=timezone.now)
    MARITAL_STATUS = models.CharField(
        max_length=2,
        choices=MARITAL_STATUS_CHOICES,
        default=SINGLE,
    )
    Gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default=MALE,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.Employee.username


class PersonalImage(models.Model):
    Employee = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profileimage/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Employee.username

    @receiver(post_save, sender=get_user_model())
    def create_PersonalImage(sender, instance, created, **kwargs):
        if created:
            PersonalImage.objects.create(Employee=instance)
            

    

class BankAccount(models.Model):
    Employee = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_account',)
    Bank_Name = models.CharField(max_length=50, blank=True, null=True)
    Account_Number = models.CharField(max_length=50, blank=True, null=True)
    Branch_Name = models.CharField(max_length=50, blank=True, null=True)
    IFSC_Code = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Employee.username

class Experience(models.Model):
    Employee = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_experience',)
    Previous_Company_Name = models.CharField(max_length=50, blank=True, null=True)
    Job_Title = models.CharField(max_length=50, blank=True, null=True)
    From = models.DateField(auto_now=False, auto_now_add=False,  default=timezone.now)
    To = models.DateField(auto_now=False, auto_now_add=False,  default=timezone.now)
    Job_Description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Employee.username


class Education(models.Model):
    Employee = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_education',)
    School_Name = models.CharField(max_length=50, blank=True, null=True)
    Degree_Or_Diploma = models.CharField(max_length=50, blank=True, null=True)
    Field_Of_Study = models.CharField(max_length=50, blank=True, null=True)
    Date_Of_Completion = models.DateField(auto_now=False, auto_now_add=False,  default=timezone.now)
    Interests = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Employee.username