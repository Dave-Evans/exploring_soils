import requests
import datetime
from decouple import config, Csv

from wisccc.models import SurveyFarm, SurveyField, FieldFarm, AncillaryData

lambda_url = config("GDU_LAMBDA_URL")


def get_collection_date(survey_field_id):
    """Get Biomass collection date from ancillary data.
    Takes the survey_field id and looks up the collection date
     from wisccc_ancillarydata"""
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            select biomass_collection_date
            from wisccc_ancillarydata
            where survey_field_id = {survey_field_id}"""
        )
        row = cursor.fetchone()
    if row == None:
        return None
    collection_date = row[0]
    return collection_date


def check_if_col_exists(field_name):
    """creates column if not existant"""
    from django.db import connection

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                select {field_name}
                from all_lab_data_2023 lab 
                """
            )
    except:
        print("Creating...")
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                ALTER TABLE all_lab_data_2023
                    ADD COLUMN IF NOT EXISTS {field_name} float8;
                """
            )


def update_record(id, column_name, val):

    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
                update all_lab_data_2023
                set {column_name} = {val}
                where id = {id}
            """
        )


def update_static_record(static_id, column_name, val):

    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
                update wisc_cc
                set {column_name} = {val}
                where id = '{static_id}'
            """
        )


def gather_gdu_precip_2023plus():

    # If survey year is before 2023 then we skip and handle elsewhere.
    # These years had poorly formed dates.
    survey_fields = SurveyField.objects.filter(survey_farm__survey_year__gt=2022)

    for survey_field in survey_fields:

        print(survey_field.id)
        print("\tFall...")
        grab_and_update_weather_dat(survey_field, "fall")
        print("\tSpring...")
        grab_and_update_weather_dat(survey_field, "spring")


def grab_and_update_weather_dat(survey_field_instance, season="fall"):

    cc_planting_date = survey_field_instance.cover_crop_planting_date
    if season == "fall":
        cc_collection = (
            AncillaryData.objects.filter(survey_field_id=survey_field_instance.id)
            .first()
            .biomass_collection_date
        )
    else:
        cc_collection = (
            AncillaryData.objects.filter(survey_field_id=survey_field_instance.id)
            .first()
            .spring_biomass_collection_date
        )
    field_location = (
        FieldFarm.objects.filter(id=survey_field_instance.field_farm_id)
        .first()
        .field_location
    )

    if all([cc_planting_date, cc_collection, field_location]):

        # start_date = cc_planting_date.strftime("%Y-%m-%d")
        start_date = cc_planting_date
        end_date = cc_collection.strftime("%Y-%m-%d")
        lon = field_location.coords[0]
        lat = field_location.coords[1]
    else:
        print("can't calc GDU")
        print(f"\tPlanting date {cc_planting_date}")
        print(f"\tcc_collection: {cc_collection}")
        print(f"\tFarm location: {field_location}")
        return None

    data = {
        "lon": lon,
        "lat": lat,
        "start_date": start_date,
        "end_date": end_date,
    }
    gdu = calc_gdu(data)
    precip = calc_precip(data)
    try:
        ancillary_data = AncillaryData.objects.get(
            survey_field_id=survey_field_instance.id
        )
    except:
        print("No Ancillary data record for survey_field:", survey_field_instance.id)
        return None

    if season == "fall":
        ancillary_data.acc_gdd = gdu
        ancillary_data.total_precip = precip
    else:
        ancillary_data.spring_acc_gdd = gdu
        ancillary_data.spring_total_precip = precip

    ancillary_data.save()


def calc_gdu(data):

    headers = {"Accept": "application/json"}

    data["target"] = "GDU"

    resp = requests.get(
        lambda_url,
        headers=headers,
        data=data,
    )
    gdu = None
    if resp.status_code == 200 or resp.text != "null":
        gdu = resp.json()["body"]["cumulative_gdd"]
    else:
        print("Error: " + resp.text)

    return gdu


def calc_precip(data):

    headers = {"Accept": "application/json"}

    data["target"] = "PRE"

    resp = requests.get(
        lambda_url,
        headers=headers,
        data=data,
    )
    total_precip = None
    if resp.status_code == 200 or resp.text != "null":
        total_precip = resp.json()["body"]["cumulative_precip"]
    else:
        print("Error: " + resp.text)

    return total_precip


def update_gdu_precip_2020_2022():
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("select * from wisc_cc")
        wisc_cc = cursor.fetchall()

    for i, cc in enumerate(wisc_cc):
        # if i < 10:
        #     continue
        lat = cc[21]
        lon = cc[22]
        cc_planting_date = cc[23]
        cc_biomass_collection = cc[25]

        if not all([lat, lon, cc_planting_date, cc_biomass_collection]):
            print("Null for", cc[1])
            print([lat, lon, cc_planting_date, cc_biomass_collection])
            continue
        start_date = cc_planting_date.strftime("%Y-%m-%d")
        end_date = cc_biomass_collection.strftime("%Y-%m-%d")
        old_precip = cc[26]
        old_gdu = cc[27]

        static_id = cc[1]
        data = {
            "lon": lon,
            "lat": lat,
            "start_date": start_date,
            "end_date": end_date,
        }
        # calc precip
        total_precip = calc_precip(data)
        # calc gdu
        gdu = calc_gdu(data)

        print("Old => new")
        print(f"{old_precip} => {total_precip}")
        print(f"{old_gdu} => {gdu}")
        # update
        update_static_record(static_id, "total_precip", total_precip)
        update_static_record(static_id, "acc_gdd", gdu)
