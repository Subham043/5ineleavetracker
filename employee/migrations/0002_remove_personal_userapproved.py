# Generated by Django 3.2 on 2021-04-29 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personal',
            name='UserApproved',
        ),
    ]
