# Generated by Django 3.2 on 2021-05-11 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0011_applyleave_rejected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyleave',
            name='Reason_For_Leave',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='applyleave',
            name='Reason_For_Rejection',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]