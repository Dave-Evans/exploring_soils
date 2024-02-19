import requests
from decouple import config, Csv

from wisccc.models import Survey

lambda_url = config("GDU_LAMBDA_URL")


def get_collection_date(id):
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            select 
            TO_DATE(lab.date_processed,'MM-DD-YYYY') as cc_biomass_collection_date
            from all_lab_data_2023 lab 
            where id = {id}"""
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


check_if_col_exists("acc_gdd")
check_if_col_exists("total_precip")

surveys = Survey.objects.all()

for srvy in surveys:
    print(srvy.id)

    cc_planting_date = srvy.cover_crop_planting_date
    cc_collection = get_collection_date(srvy.id)
    farm_location = srvy.farm_location

    if all([cc_planting_date, cc_collection, farm_location]):

        start_date = cc_planting_date.strftime("%Y-%m-%d")
        end_date = cc_collection.strftime("%Y-%m-%d")
        lon = farm_location.coords[0]
        lat = farm_location.coords[1]
    else:
        print("can't calc GDU")
        print(f"\tPlanting date {cc_planting_date}")
        print(f"\tcc_collection: {cc_collection}")
        print(f"\tFarm location: {farm_location}")
        continue

    headers = {"Accept": "application/json"}

    data = {
        "target": "GDU",
        "lon": lon,
        "lat": lat,
        "start_date": start_date,
        "end_date": end_date,
    }
    resp = requests.get(
        lambda_url,
        headers=headers,
        data=data,
    )
    gdu = None
    if resp.status_code == 200:
        gdu = resp.json()["body"]["cumulative_gdd"]
    else:
        print("Error: " + resp.text)

    if gdu is not None:
        update_record(srvy.id, "acc_gdd", gdu)

    data = {
        "target": "PRE",
        "lon": lon,
        "lat": lat,
        "start_date": start_date,
        "end_date": end_date,
    }

    resp = requests.get(
        lambda_url,
        headers=headers,
        data=data,
    )
    if resp.status_code == 200:
        precip = resp.json()["body"]["cumulative_precip"]
    else:
        print("Error: " + resp.text)

    if precip is not None:
        update_record(srvy.id, "total_precip", precip)
