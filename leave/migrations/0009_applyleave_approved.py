# Generated by Django 3.2 on 2021-05-11 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0008_holidaylist'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyleave',
            name='Approved',
            field=models.BooleanField(default=False),
        ),
    ]
