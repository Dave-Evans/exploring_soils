import django_tables2 as tables
from django_tables2 import TemplateColumn

from kanopy.models import Groundcoverdoc


class KanopyTable(tables.Table):

    class Meta:
        model = Groundcoverdoc
        fields = ('locname', 'description', 'image', 'collectionpoint')
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-hover"}

    # edit = TemplateColumn(template_name='bikemileage/mileage_update_column.html')
    # delete = TemplateColumn(template_name='bikemileage/mileage_delete_column.html')
