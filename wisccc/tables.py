import django_tables2 as tables
from django_tables2 import TemplateColumn
from django.db import connection
import itertools
import pandas as pd
from wisccc.models import Survey, Farmer, SurveyRegistration, SurveyField

class ScenarioTable(tables.Table):
    row_number = tables.Column(empty_values=())
    # survey_field__survey_farm__id = tables.Column()
    survey_field__crop_rotation_2023_cash_crop_species = tables.Column()
    survey_field__cash_crop_planting_date = tables.Column()
    # survey_field__cover_crop_species_1 = tables.Column()
    survey_field__cover_crop_seeding_method = tables.Column()
    survey_field__cover_crop_planting_date = tables.Column()
    survey_field__manure_prior = tables.Column(verbose_name="Manure added before cover?")
    # survey_field__tillage_system_cash_crop = tables.Column()
    cc_biomass = tables.Column()
    total_nitrogen = tables.Column()
    # def render_cover_crop_species(self, record):
        # return ", ".join(record.cover_crop_species_1 + record.cover_crop_species_2, record.cover_crop_species_3 + record.cover_crop_species_4, record.cover_crop_species_5)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return f"{next(self.counter) + 1}"
    
    class Meta:
        orderable = False

class ResponseTable(tables.Table):
    farmer__first_name = tables.Column()
    farmer__last_name = tables.Column()
    # username = tables.Column()
    farmer__user__email = tables.Column()
    survey_created = tables.Column()
    edit = TemplateColumn(template_name="wisccc/update_column_response.html")
    upload_photo = TemplateColumn(template_name="wisccc/upload_photo_column.html")
    update_labdata = TemplateColumn(
        template_name="wisccc/update_column_ancillarydata.html"
    )
    # delete = TemplateColumn(template_name="wisccc/delete_column.html")

    class Meta:
        template_name = "django_tables2/bootstrap4.html"

        attrs = {"class": "table table-hover"}

        row_attrs = {
            # For highlighting rows according to if confirmed good
            "class": lambda record: (
                "table-success"
                if record.confirmed_accurate == True
                else (
                    "table-danger"
                    if record.confirmed_accurate == False
                    else "table-warning"
                )
            )
        }


class RegistrationTable(tables.Table):
    signup_timestamp = tables.Column()
    farmer__first_name = tables.Column()
    farmer__last_name = tables.Column()
    farmer__user__email = tables.Column()
    belong_to_groups = tables.Column()
    notes = tables.Column()
    edit = TemplateColumn(template_name="wisccc/update_column_registration.html")
    delete = TemplateColumn(template_name="wisccc/delete_registration_column.html")

    class Meta:

        template_name = "django_tables2/bootstrap4.html"

        attrs = {"class": "table table-hover"}


class ResearcherTable(tables.Table):

    first_name = tables.Column()
    last_name = tables.Column()
    email = tables.Column()
    # username = tables.Column()
    signup_timestamp = tables.Column()
    institution = tables.Column()
    agreement_doc = tables.Column()
    notes = tables.Column()
    approved = tables.Column()
    approved_date = tables.Column()
    number_of_downloads = tables.Column()
    last_downloaded = tables.Column()
    edit = TemplateColumn(template_name="wisccc/update_column_researcher.html")
    delete = TemplateColumn(template_name="wisccc/delete_researcher_column.html")

    class Meta:

        template_name = "django_tables2/bootstrap4.html"

        attrs = {"class": "table table-hover"}


class InterestedPartyTable(tables.Table):

    signup_timestamp = tables.Column()
    first_name = tables.Column()
    last_name = tables.Column()
    email = tables.Column()
    cover_crops_interest = tables.Column()
    admin_notes = tables.Column()

    edit = TemplateColumn(template_name="wisccc/update_column_interested_party.html")
    delete = TemplateColumn(template_name="wisccc/delete_column_interested_party.html")


class InterestedAgronomistTable(tables.Table):

    signup = tables.Column()
    first_name = tables.Column()
    last_name = tables.Column()
    email = tables.Column()

    availability = tables.Column()
    admin_notes = tables.Column()

    edit = TemplateColumn(
        template_name="wisccc/update_column_interested_agronomist.html"
    )
    delete = TemplateColumn(
        template_name="wisccc/delete_column_interested_agronomist.html"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columns["signup"].column.attrs = {"td": {"style": "width:12%;"}}
        self.columns["first_name"].column.attrs = {"td": {"style": "width:10%;"}}
        self.columns["last_name"].column.attrs = {"td": {"style": "width:10%;"}}
