# Generated by Django 3.2 on 2021-04-29 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuth', '0001_initial'),
        ('employee', '0004_alter_personal_userapproved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal',
            name='userApproved',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved', to='UserAuth.userapproved'),
        ),
    ]
