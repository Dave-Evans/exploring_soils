from django_filters import FilterSet
import django_filters
from .models import Mileage


class MileageFilter(FilterSet):

    ride_date = django_filters.DateTimeFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={'class': 'datepicker'}
        )
    )

    class Meta:
        model = Mileage
        # fields = {"ride_date" : ride_date, "bike_type": ["exact"], "rider": ["exact"]}
        fields = ['ride_date', 'bike_type', 'rider']
