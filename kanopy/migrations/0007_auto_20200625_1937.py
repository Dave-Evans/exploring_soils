# Generated by Django 3.0 on 2020-06-26 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanopy', '0006_groundcoverdoc_fgcc_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groundcoverdoc',
            name='fgcc_value',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10),
        ),
    ]