# Generated by Django 3.2 on 2021-05-14 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuth', '0004_auto_20210508_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='LeaveStatus',
            field=models.BooleanField(default=False),
        ),
    ]
