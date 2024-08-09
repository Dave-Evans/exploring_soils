import django_tables2 as tables
from django_tables2 import TemplateColumn


class ResponseTable(tables.Table):
    first_name = tables.Column()
    last_name = tables.Column()
    # username = tables.Column()
    email = tables.Column()
    survey_created = tables.Column()
    edit = TemplateColumn(template_name="wisccc/update_column_response.html")
    upload_photo = TemplateColumn(template_name="wisccc/upload_photo_column.html")
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

        # row_attrs = {
        #     # For highlighting rows according to if confirmed good
        #     "class": lambda record: (
        #         "table-success"
        #         if record["confirmed_accurate"] == True
        #         else (
        #             "table-danger"
        #             if record["confirmed_accurate"] == False
        #             else "table-warning"
        #         )
        #     )
        # }
