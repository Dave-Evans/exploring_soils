# Generated by Django 2.1 on 2020-03-28 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bikemileage', '0007_auto_20200220_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bicycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('make', models.CharField(default='Unknown', max_length=30)),
                ('model', models.CharField(default='Unknown', max_length=30)),
                ('year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bicycles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]