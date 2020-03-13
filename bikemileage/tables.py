import django_tables2 as tables

from .models import Mileage


class Bootstrap4Table(tables.Table):
    # country = tables.Column(linkify=True)
    # continent = tables.Column(accessor="country__continent", linkify=True)

    class Meta:
        model = Mileage
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-hover"}
        # exclude = ("friendly",)

