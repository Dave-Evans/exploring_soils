# Generated by Django 2.1 on 2020-01-19 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20200119_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='finished_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='publication_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]