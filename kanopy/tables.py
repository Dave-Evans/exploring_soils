import django_tables2 as tables
from django_tables2 import TemplateColumn

from kanopy.models import Groundcoverdoc

class KanopyTable(tables.Table):

    class Meta:
        model = Groundcoverdoc
        fields = (
            'location_name', 
            'uploaded_at',
            'image',
            'contact_email',
            'comments'
        )
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-hover"}
        
    # edit = TemplateColumn(template_name='kanopy/update_column.html')
    delete = TemplateColumn(template_name='kanopy/delete_column.html')


class KanopyTableFull(tables.Table):

    class Meta:
        model = Groundcoverdoc
        fields = (
            'location_name', 
            'cover_crop_species_1',
            'cover_crop_species_2',
            'cover_crop_species_3',
            'cover_crop_species_4',
            'cover_crop_planting_date',
            'cover_crop_planting_rate',
            'cover_crop_interseeded',
            'crop_prior',
            'crop_posterior',
            'seeding_method',
            'cover_crop_termination_date',
            'photo_taken_date',
            'image',
            'collectionpoint',
            'fgcc_value',
            'comments',
            'contact_email'
        )
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-hover"}

    # edit = TemplateColumn(template_name='bikemileage/mileage_update_column.html')
    # delete = TemplateColumn(template_name='bikemileage/mileage_delete_column.html')
