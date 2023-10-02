import django_tables2 as tables
from django_tables2 import TemplateColumn
from django.db import connection
import pandas as pd
from wisccc.models import Survey, Farmer


def get_table_data():
    """For getting survey data and returning an excel doc"""
    query = """
        select 
            s.id as response_id
            , u.username 
            , u.email
            , f.first_name 
            , f.last_name
            , s.survey_created
        from wisccc_survey s 
        left join wisccc_farmer f
        on s.user_id = f.user_id 
        left join auth_user as u
        on s.user_id = u.id"""
    dat = pd.read_sql(query, connection)
    return dat


data = get_table_data()


class ResponseTable(tables.Table):
    # id = tables.Column()
    username = tables.Column()
    # first_name = tables.Column()
    # last_name = tables.Column()
    email = tables.Column()
    survey_created = tables.Column()
    # class Meta:
    #     model = Survey
    #     fields = ("username", "first_name", "last_name", "email", "survey_created")
    #     template_name = "django_tables2/bootstrap.html"
    #     attrs = {"class": "table table-hover"}

    # edit = TemplateColumn(template_name="wisccc/update_column.html")
    delete = TemplateColumn(template_name="wisccc/delete_column.html")


# table = ResponseTable(data)
