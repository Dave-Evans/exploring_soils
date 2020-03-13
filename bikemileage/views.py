from random import choice

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.template import loader

from django.views.generic.base import TemplateView
from django_filters.views import FilterView

from django_tables2 import MultiTableMixin, RequestConfig, SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin
from django_tables2.paginators import LazyPaginator

from .filters import MileageFilter
from .models import Mileage
from .tables import (
    Bootstrap4Table,
)


def mileage_list(request):
    """List mileage entries"""

    table = Bootstrap4Table(Mileage.objects.all(), order_by="-ride_date")
    RequestConfig(request, paginate={"per_page": 100}).configure(table)

    return render(request, "bikemileage/bootstrap4_template.html", {"table": table})




class CustomMileageListView(ExportMixin, SingleTableMixin, FilterView):
    """List mileage entries, with filters"""
    table_class = Bootstrap4Table
    model = Mileage
    template_name = "bikemileage/bootstrap4_template.html"

    filterset_class = MileageFilter

    export_formats = ("csv", "xls")

    def get_queryset(self):
        return super().get_queryset()#.select_related("bike_type")

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}





