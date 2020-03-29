import django_tables2 as tables
from django_tables2 import TemplateColumn

from .models import Mileage


class Bootstrap4Table(tables.Table):

    class Meta:
        model = Mileage
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-hover"}

    edit = TemplateColumn(template_name='bikemileage/mileage_update_column.html')
    delete = TemplateColumn(template_name='bikemileage/mileage_delete_column.html')
