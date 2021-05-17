# Generated by Django 3.2 on 2021-05-10 13:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0007_auto_20210510_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='HolidayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Date', models.DateField(default=django.utils.timezone.now)),
                ('Description', models.TextField(blank=True, default='', null=True)),
                ('Type', models.CharField(choices=[('EVENT', 'Event'), ('HOLIDAY', 'Holiday')], default='HOLIDAY', max_length=8)),
                ('EveryYear', models.BooleanField(default=False)),
            ],
        ),
    ]