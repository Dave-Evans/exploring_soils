from random import choice

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.template import loader


from django.views.generic.base import TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django_tables2 import (
    MultiTableMixin,
    RequestConfig,
    SingleTableMixin,
    SingleTableView,
)
from django_tables2.export.views import ExportMixin
from django_tables2.paginators import LazyPaginator

from .forms import MileageForm
from .filters import MileageFilter
from .models import Mileage, Bicycle
from .tables import (
    Bootstrap4Table,
)


def mileage_list(request):
    """List mileage entries"""

    table = Bootstrap4Table(Mileage.objects.all(), order_by="-ride_date")
    RequestConfig(request, paginate={"per_page": 100}).configure(table)

    return render(request, "bikemileage/bootstrap4_template.html", {"table": table})


@method_decorator(login_required, name="dispatch")
class MileageCreateView(CreateView):
    model = Mileage
    fields = ("ride_date", "mileage", "bike_type", "comment", "cost")

    def form_valid(self, form):
        mileage = form.save(commit=False)
        mileage.rider = self.request.user
        mileage.save()
        return redirect("custom_mileage")


# TODO: add a 'cancel' button to the update page, where is that update page?
@method_decorator(login_required, name="dispatch")
class MileageUpdateView(UpdateView):
    model = Mileage
    form_class = MileageForm
    template_name = "bikemileage/mileage_update_form.html"


@method_decorator(login_required, name="dispatch")
class MileageDeleteView(DeleteView):
    model = Mileage
    # template_name = 'bikemileage/mileage_update_form.html'
    success_url = reverse_lazy("custom_mileage")


@method_decorator(login_required, name="dispatch")
class CustomMileageListView(ExportMixin, SingleTableMixin, FilterView):
    """List mileage entries, with filters"""

    table_class = Bootstrap4Table
    model = Mileage
    template_name = "bikemileage/bootstrap4_template.html"

    filterset_class = MileageFilter

    export_formats = ("csv", "xls")

    def get_queryset(self):
        return super().get_queryset().filter(rider=self.request.user)

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}


class BicycleListView(LoginRequiredMixin, ListView):
    model = Bicycle
    context_object_name = "bicycles"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class BicycleCreateView(LoginRequiredMixin, CreateView):
    model = Bicycle
    fields = ["name", "make", "model", "year"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BicycleUpdateView(UpdateView):
    model = Bicycle
    fields = ["name", "make", "model", "year"]


class BicycleDeleteView(DeleteView):
    model = Bicycle
    success_url = reverse_lazy("bicycle_list")


"""
def bicycle_create(request):
    bicycles = Bicycle.objects.all()
    bicycles = bicycles.order_by("name")
    return render(request, 'bikemileage/bicycle_create.html', {'bicycles': bicycles})


def bicycle_update(request, pk):
    bicycles = Bicycle.objects.all()
    bicycles = bicycles.order_by("name")
    return render(request, 'bikemileage/bicycle_update.html', {'bicycles': bicycles})


def bicycle_delete(request, pk):
    bicycles = Bicycle.objects.all()
    bicycles = bicycles.order_by("name")
    return render(request, 'bikemileage/bicycle_delete.html', {'bicycles': bicycles})
"""
