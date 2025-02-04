import django_tables2 as tables
from django_tables2 import TemplateColumn
from django.db import connection
import pandas as pd
from wisccc.models import Survey, Farmer, SurveyRegistration


class ResponseTable(tables.Table):
    first_name = tables.Column()
    last_name = tables.Column()
    # username = tables.Column()
    email = tables.Column()
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
                if record["confirmed_accurate"] == True
                else (
                    "table-danger"
                    if record["confirmed_accurate"] == False
                    else "table-warning"
                )
            )
        }


class RegistrationTable(tables.Table):
    signup_timestamp = tables.Column()
    first_name = tables.Column()
    last_name = tables.Column()
    email = tables.Column()
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
