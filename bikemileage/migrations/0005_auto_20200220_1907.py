# Generated by Django 2.1 on 2020-02-21 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bikemileage', '0004_auto_20200219_1948'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mileage',
            old_name='date',
            new_name='ride_date',
        ),
    ]
