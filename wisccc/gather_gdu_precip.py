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
                COALESCE(
                    TO_DATE(lab.date_reported_biomass,'YYYY-MM-DD'),
                    TO_DATE(lab.date_processed,'YYYY-MM-DD')
                ) as cc_biomass_collection_date
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
        if resp.status_code == 200 or resp.text != "null":
            gdu = resp.json()["body"]["cumulative_gdd"]
        else:
            print("Error: " + resp.text)

        if gdu is not None:
            update_record(srvy.id, "acc_gdd", round(gdu, 1))

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
        if i < 10:
            continue
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
