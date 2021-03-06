# Generated by Django 3.0 on 2020-07-18 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanopy', '0003_auto_20200714_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='groundcoverdoc',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='groundcoverdoc',
            name='cover_crop_species_1',
            field=models.CharField(choices=[('NONE', ''), ('ALFALFA', 'Alfalfa (Medicago sativa)'), ('ANNUAL_RYE', 'Annual Rye (Lolium multiflorum'), ('BUCKWHEAT', 'Buckweat (Fagopyrum esculentum)'), ('CAMELINA', 'Camelina (Camelina sativa)'), ('CEREAL_RYE', 'Cereal Rye (Secale cereale)'), ('COWPEAS', 'Cowpeas (Vigna unguiculata)'), ('CRIMSON_CLOVER', 'Crimson Clover (Trifolium incarnatum)'), ('HAIRY_VETCH', 'Hairy Vetch (Vicia villosa)'), ('MUSTARDS', 'Mustartds (Brassicaceae)'), ('OATS', 'Oats (Avena sativa)'), ('PENNYCRESS', 'Pennycress (Thlaspi arvense)'), ('RADISH', 'Radish (Raphanus sativus)'), ('RAPESEED', 'Rapeseed (Brassica napus)'), ('RED_CLOVER', 'Red Clover (Trifolium pratense)'), ('SUNN_HEMP', 'Sunn Hemp (Crotalaria juncea)'), ('TURNIP', 'Turnip (Brassica rapa var. rapa)'), ('WHITE_CLOVER', 'White Clover (Trifolium repens)'), ('OTHER', 'Other')], max_length=25),
        ),
        migrations.AlterField(
            model_name='groundcoverdoc',
            name='cover_crop_species_2',
            field=models.CharField(blank=True, choices=[('NONE', ''), ('ALFALFA', 'Alfalfa (Medicago sativa)'), ('ANNUAL_RYE', 'Annual Rye (Lolium multiflorum'), ('BUCKWHEAT', 'Buckweat (Fagopyrum esculentum)'), ('CAMELINA', 'Camelina (Camelina sativa)'), ('CEREAL_RYE', 'Cereal Rye (Secale cereale)'), ('COWPEAS', 'Cowpeas (Vigna unguiculata)'), ('CRIMSON_CLOVER', 'Crimson Clover (Trifolium incarnatum)'), ('HAIRY_VETCH', 'Hairy Vetch (Vicia villosa)'), ('MUSTARDS', 'Mustartds (Brassicaceae)'), ('OATS', 'Oats (Avena sativa)'), ('PENNYCRESS', 'Pennycress (Thlaspi arvense)'), ('RADISH', 'Radish (Raphanus sativus)'), ('RAPESEED', 'Rapeseed (Brassica napus)'), ('RED_CLOVER', 'Red Clover (Trifolium pratense)'), ('SUNN_HEMP', 'Sunn Hemp (Crotalaria juncea)'), ('TURNIP', 'Turnip (Brassica rapa var. rapa)'), ('WHITE_CLOVER', 'White Clover (Trifolium repens)'), ('OTHER', 'Other')], max_length=25),
        ),
        migrations.AlterField(
            model_name='groundcoverdoc',
            name='cover_crop_species_3',
            field=models.CharField(blank=True, choices=[('NONE', ''), ('ALFALFA', 'Alfalfa (Medicago sativa)'), ('ANNUAL_RYE', 'Annual Rye (Lolium multiflorum'), ('BUCKWHEAT', 'Buckweat (Fagopyrum esculentum)'), ('CAMELINA', 'Camelina (Camelina sativa)'), ('CEREAL_RYE', 'Cereal Rye (Secale cereale)'), ('COWPEAS', 'Cowpeas (Vigna unguiculata)'), ('CRIMSON_CLOVER', 'Crimson Clover (Trifolium incarnatum)'), ('HAIRY_VETCH', 'Hairy Vetch (Vicia villosa)'), ('MUSTARDS', 'Mustartds (Brassicaceae)'), ('OATS', 'Oats (Avena sativa)'), ('PENNYCRESS', 'Pennycress (Thlaspi arvense)'), ('RADISH', 'Radish (Raphanus sativus)'), ('RAPESEED', 'Rapeseed (Brassica napus)'), ('RED_CLOVER', 'Red Clover (Trifolium pratense)'), ('SUNN_HEMP', 'Sunn Hemp (Crotalaria juncea)'), ('TURNIP', 'Turnip (Brassica rapa var. rapa)'), ('WHITE_CLOVER', 'White Clover (Trifolium repens)'), ('OTHER', 'Other')], max_length=25),
        ),
        migrations.AlterField(
            model_name='groundcoverdoc',
            name='cover_crop_species_4',
            field=models.CharField(blank=True, choices=[('NONE', ''), ('ALFALFA', 'Alfalfa (Medicago sativa)'), ('ANNUAL_RYE', 'Annual Rye (Lolium multiflorum'), ('BUCKWHEAT', 'Buckweat (Fagopyrum esculentum)'), ('CAMELINA', 'Camelina (Camelina sativa)'), ('CEREAL_RYE', 'Cereal Rye (Secale cereale)'), ('COWPEAS', 'Cowpeas (Vigna unguiculata)'), ('CRIMSON_CLOVER', 'Crimson Clover (Trifolium incarnatum)'), ('HAIRY_VETCH', 'Hairy Vetch (Vicia villosa)'), ('MUSTARDS', 'Mustartds (Brassicaceae)'), ('OATS', 'Oats (Avena sativa)'), ('PENNYCRESS', 'Pennycress (Thlaspi arvense)'), ('RADISH', 'Radish (Raphanus sativus)'), ('RAPESEED', 'Rapeseed (Brassica napus)'), ('RED_CLOVER', 'Red Clover (Trifolium pratense)'), ('SUNN_HEMP', 'Sunn Hemp (Crotalaria juncea)'), ('TURNIP', 'Turnip (Brassica rapa var. rapa)'), ('WHITE_CLOVER', 'White Clover (Trifolium repens)'), ('OTHER', 'Other')], max_length=25),
        ),
    ]
