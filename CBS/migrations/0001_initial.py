# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 10:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bike_name', models.CharField(max_length=100)),
                ('in_use', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Bike',
                'verbose_name_plural': 'Bikes',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('booking_end_time', models.DateTimeField(null=True)),
                ('booking_bike', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CBS.Bike')),
            ],
            options={
                'verbose_name': 'Booking',
                'verbose_name_plural': 'Bookings',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.CharField(max_length=100)),
                ('station_address', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name': 'Station',
                'verbose_name_plural': 'Stations',
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CBS.Station'),
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bike',
            name='station_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CBS.Station'),
        ),
    ]