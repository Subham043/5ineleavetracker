# Generated by Django 3.2 on 2021-05-10 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0005_auto_20210510_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaveavailable',
            name='leavetype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave.leavetype'),
        ),
    ]
