from django_filters import FilterSet
import django_filters
from .models import SurveyFarm, Farmer, SurveyRegistration, SurveyField


class SurveyResponseFilter(FilterSet):

    # survey_year = django_filters.NumberFilter(lookup_expr="iexact")
    survey_farm__farmer__last_name = django_filters.CharFilter(lookup_expr="icontains", label="Farmer last name")
    survey_farm__farmer__user__email = django_filters.CharFilter(lookup_expr="icontains", label="Farmer email")
    survey_farm__survey_year = django_filters.NumberFilter(lookup_expr="exact", label="Year in which survey was released")
    survey_farm__farmer__id = django_filters.NumberFilter(lookup_expr="exact", label="Farmer ID number")
    survey_farm__id = django_filters.NumberFilter(lookup_expr="exact", label="ID number for survey farm")
    id = django_filters.NumberFilter(lookup_expr="exact", label="ID number for survey field (on scenario cards)")

    # class Meta:
        # model = SurveyField
        # fields = [
            # "survey_farm__survey_year",
            # "survey_farm__farmer__id",
            # "id"
            # "farmer__user__email",
            # "farmer__last_name",
        # ]


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
