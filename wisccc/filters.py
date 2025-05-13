from django_filters import FilterSet
import django_filters
from .models import SurveyFarm, Farmer, SurveyRegistration


class SurveyResponseFilter(FilterSet):

    # survey_year = django_filters.NumberFilter(lookup_expr="iexact")
    farmer__last_name = django_filters.CharFilter(lookup_expr="icontains")
    farmer__user__email = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = SurveyFarm
        fields = [
            "survey_year",
            "farmer__id",
            # "farmer__user__email",
            # "farmer__last_name",
        ]


class SurveyRegistrationFilter(FilterSet):

    # survey_year = django_filters.NumberFilter(lookup_expr="iexact")
    farmer__last_name = django_filters.CharFilter(lookup_expr="icontains")
    farmer__user__email = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = SurveyRegistration
        fields = [
            "survey_year",
            "farmer__id",
            # "farmer__user__email",
            # "farmer__last_name",
        ]
