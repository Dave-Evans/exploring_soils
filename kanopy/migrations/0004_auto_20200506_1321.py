# Generated by Django 2.2 on 2020-05-06 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanopy', '0003_auto_20200506_1313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groundcoverdoc',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='groundcoverdoc',
            name='longitude',
        ),
    ]