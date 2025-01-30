import requests
import datetime
from decouple import config, Csv

from wisccc.models import SurveyFarm, SurveyField, FieldFarm, AncillaryData

lambda_url = config("GDU_LAMBDA_URL")

import requests
import math

# import geopandas
# from shapely.geometry import Point
import datetime
import json
import logging


class RetrieveACIS:

    def __init__(self):
        self.url_station_meta = "https://data.rcc-acis.org/StnMeta"
        self.url_station_collect = "https://data.rcc-acis.org/StnData"
        self.list_stations = self.get_stations()
        self.sorted_list_stations = []

    # Look up stations
    def get_stations(self):

        headers = {"Accept": "application/json"}
        params = {
            # Bounding box for just WI
            "bbox": "-86,41.5,-93.5,48",
            "meta": "name,sids,ll,valid_daterange",
            "elems": "pcpn",
        }

        response = requests.post(
            self.url_station_meta,
            data={"params": json.dumps(params)},
            headers={"Accept": "application/json"},
        )
        try:
            rslt = response.json()
        except:
            print("Failed getting json.")
            print(response.text)
            return None
        rslt_meta = rslt["meta"]

        # This would be the min of all planting dates
        target_date = datetime.datetime(2022, 1, 1)
        list_stations = []
        for station in rslt_meta:
            end_valid_date = datetime.datetime.strptime(
                station["valid_daterange"][0][1], "%Y-%m-%d"
            )
            if target_date > end_valid_date:
                print(f"\n{station['name']} outside valid date range")
            else:
                list_stations.append(station)

        return list_stations

    def calc_dist(self, lon1, lat1, lon2, lat2):
        """For calculating the distance between two points
        powerappsguide.com/blog/post/formulas-calculate-the-distance-between-2-points-longitude-latitude
        returns distance in km
        """
        r = 6371  # radius of Earth (KM)
        p = 0.017453292519943295  # Pi/180
        a = (
            0.5
            - math.cos((lat2 - lat1) * p) / 2
            + math.cos(lat1 * p)
            * math.cos(lat2 * p)
            * (1 - math.cos((lon2 - lon1) * p))
            / 2
        )

        d = 2 * r * math.asin(math.sqrt(a))  # 2*R*asin

        return d

    # find nearest station to covercrop location
    def get_dist_to_stations(self, lon, lat):
        """Calculate distance to point from each station"""
        for station in self.list_stations:
            station["distance"] = self.calc_dist(
                station["ll"][0], station["ll"][1], lon, lat
            )

        # sort by distance, smallest to largest
        return sorted(self.list_stations, key=lambda d: d["distance"])

    # collect data from that station
    def retrieve_station_data_precip(
        self,
        stationid,
        start_date,
        end_date,
        null_threshold=0.1,
    ):
        logging.info(f"stationid: {stationid}")
        logging.info(f"start_date: {start_date}")
        logging.info(f"end_date: {end_date}")
        logging.info(f"null_threshold: {null_threshold}")

        null_threshold_cnt = round(
            null_threshold
            * (
                datetime.datetime.strptime(end_date, "%Y-%m-%d")
                - datetime.datetime.strptime(start_date, "%Y-%m-%d")
            ).days
        )

        sdate = start_date
        edate = end_date
        params = {
            "sid": stationid,
            "sdate": sdate,
            "edate": edate,
            "elems": [
                {
                    "name": "pcpn",
                    "smry": {"add": "mcnt", "reduce": "sum"},
                    "smry_only": "1",
                }
            ],
        }

        resp = requests.post(
            self.url_station_collect,
            data={"params": json.dumps(params)},
            headers={"Accept": "application/json"},
        )
        resp = resp.json()
        if resp["smry"][0][1] > null_threshold_cnt:
            print(f"\tNull threshold is {null_threshold_cnt}")
            print(f"\tCount missing from station {resp['smry'][0][1]}")
            return None
        if resp == {}:
            print("No data.")
            return None

        return resp

    def calc_cum_precip(self, start_date, end_date):
        """Get cumulative precipitation
        Based on hourly data"""

        attempt = 0
        while True:
            logging.info(f"Attempt no. {attempt}")
            closest_station = self.sorted_list_stations[attempt]
            stationid = closest_station["sids"][0]
            distance = closest_station["distance"]
            logging.info(f"Pulling data from: {stationid}")
            logging.info(f"Distance away: {distance} km")

            nearest_station_data = self.retrieve_station_data_precip(
                stationid, start_date, end_date
            )
            if nearest_station_data is None:
                logging.info("No data found.")
                attempt += 1
            else:
                break

        cum_precip = nearest_station_data["smry"][0][0]
        # Result object to return
        result = {
            "dist_to_station_km": closest_station["distance"],
            "stationid": stationid,
            "cumulative_precip": cum_precip,
            "start_date": start_date,
            "end_date": end_date,
        }

        return result

    def get_weather_data(self, start_date, end_date, lon, lat, target="PRE"):
        """if target = PRE then cumulative precip
        else target = GDU then GDU
        """
        try:
            datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        except ValueError as err:
            logging.error(f"Unexpected {err=}, {type(err)=}")
            return {"error": str(err)}

        try:
            datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError as err:
            logging.error(f"Unexpected {err=}, {type(err)=}")
            return {"error": err}

        # get df of distance to all stations
        logging.info("Calculating distance from point to all stations")
        self.sorted_list_stations = self.get_dist_to_stations(lon, lat)

        result = self.calc_cum_precip(start_date, end_date)

        result["lon"] = lon
        result["lat"] = lat

        return result


"""
start_date = "2020-08-18"
end_date = "2021-04-19"
lon = -96.80417
lat = 45.5948

get_weather_data("GDU", start_date, end_date, lon, lat)
# 1561.416666

lon = -89.0252678662976
lat = 42.72918089384226
start_date = '2024-07-20'
end_date = '2024-11-05'
target ='PRE'

from acis_retrieval import *
retrieve_acis = RetrieveACIS()

# 167
lon = -88.47102091878997
lat = 43.4422697
start_date = '2024-07-30'
end_date = '2024-10-23'
target ='PRE'

retrieve_acis.get_weather_data(start_date, end_date, lon, lat)
"""


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
    retrieve_acis = RetrieveACIS()

    survey_fields = SurveyField.objects.filter(survey_farm__survey_year__gt=2022)

    for survey_field in survey_fields:

        print(survey_field.survey_farm.id)
        print("\tFall...")
        grab_and_update_weather_dat(survey_field, retrieve_acis, "fall")
        # print("\tSpring...")
        # grab_and_update_weather_dat(survey_field, "spring")


def grab_and_update_weather_dat(
    survey_field_instance, retrieve_acis, season="fall", mode="only_null"
):

    cc_planting_date = survey_field_instance.cover_crop_planting_date
    try:
        ancillary_data = AncillaryData.objects.get(
            survey_field_id=survey_field_instance.id
        )
    except:
        print("No Ancillary data record for survey_field:", survey_field_instance.id)
        return None

    if season == "fall":
        cc_collection = ancillary_data.biomass_collection_date
    else:
        cc_collection = ancillary_data.spring_biomass_collection_date

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

    if season == "fall":
        # if ancillary_data.acc_gdd is None:
        #     ancillary_data.acc_gdd = calc_gdu(data)

        if ancillary_data.total_precip is None:
            result = retrieve_acis.get_weather_data(start_date, end_date, lon, lat)
            ancillary_data.total_precip = float(result["cumulative_precip"])
    else:
        if ancillary_data.spring_acc_gdd is None:
            ancillary_data.spring_acc_gdd = calc_gdu(data)

        if ancillary_data.spring_total_precip is not None:
            ancillary_data.spring_total_precip = calc_precip(data)

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
    if resp.status_code != 200 or resp.text != "null":
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
