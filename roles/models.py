from django.db import models

# Create your models here.

class roles(models.Model):
    Role_Name = models.CharField(max_length=50, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.Role_Name