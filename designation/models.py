from django.db import models

# Create your models here.


class designation(models.Model):
    Designation_Name = models.CharField(max_length=50, blank=False, null=False)
    Stream = models.CharField(max_length=50, blank=True, null=True)
    Mail_Alias = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.Designation_Name