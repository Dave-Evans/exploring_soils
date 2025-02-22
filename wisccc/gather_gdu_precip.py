import requests
import datetime
import logging
import math
import json
from wisccc.models import SurveyFarm, SurveyField, FieldFarm, AncillaryData


class RetrieveACIS:

    def __init__(self):
        self.url_station_meta = "https://data.rcc-acis.org/StnMeta"
        self.url_station_collect = "https://data.rcc-acis.org/StnData"
        # Master list of stations, this will stay the same for the life
        #   of the object, updated with new distances
        self.list_stations_pcpn = self.get_stations("pcpn")
        self.list_stations_gdu = self.get_stations("gdd")
        # Sorted whenever a new location is queried
        self.sorted_list_stations_pcpn = []
        self.sorted_list_stations_gdu = []

    # Look up stations
    def get_stations(self, elem="pcpn"):
        # elem should be "pcpn" or "gdd"
        headers = {"Accept": "application/json"}
        params = {
            # Bounding box for just WI
            "bbox": "-86,41.5,-93.5,48",
            "meta": "name,sids,ll,valid_daterange",
            "elems": elem,
            "sdate": "2020-01-01",
            "edate": "2025-12-31",
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
        # target_date = datetime.datetime(2020, 1, 1)
        # list_stations = []
        # for station in rslt_meta:
        #     end_valid_date = datetime.datetime.strptime(
        #         station["valid_daterange"][0][1], "%Y-%m-%d"
        #     )
        #     if target_date < end_valid_date:

        #         list_stations.append(station)

        return rslt_meta

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

    def calcHeat(self, fk1, tsum, diff):
        twopi = 6.283185308
        pihlf = 1.570796327
        d2 = fk1 - tsum
        theta = math.atan(d2 / math.sqrt(diff * diff - d2 * d2))
        if (d2 < 0) & (theta > 0):
            theta = theta - math.pi

        return (diff * math.cos(theta) - d2 * (pihlf - theta)) / twopi

    def gdu_be(self, nearest_station_data, base_number=40, upper_thresh=86):
        data = nearest_station_data["data"]

        heat = 0
        fk1 = 2 * base_number

        cumulative_gdd = 0

        for datum in data:

            try:
                tmax = int(datum[1])
                tmin = int(datum[2])
            except ValueError:
                continue

            diff = tmax - tmin
            tsum = tmax + tmin

            # return 0 if invalid inputs or max below base_number
            if (tmin > tmax) | (tmax <= tmin) | (tmax <= base_number):
                gdu = 0
            elif tmin >= base_number:
                gdu = (tsum - fk1) / 2
            elif tmin < base_number:
                gdu = self.calcHeat(fk1, tsum, diff)
            elif tmax > upper_thresh:
                # fk1 = 2 * upper_thresh
                zheat = heat
                heat = self.calcHeat(2 * upper_thresh, tsum, diff)
                gdu = zheat - 2 * heat

            cumulative_gdd += gdu

        return cumulative_gdd

    # find nearest station to covercrop location
    def get_dist_to_stations(self, stnt_list, lon, lat):
        """Calculate distance to point from each station"""
        for station in stnt_list:
            station["distance"] = self.calc_dist(
                station["ll"][0], station["ll"][1], lon, lat
            )

        # sort by distance, smallest to largest
        return sorted(stnt_list, key=lambda d: d["distance"])

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
        try:
            resp = resp.json()
        except:
            print("Error converting result to json")
            print(resp.text)
        if resp["smry"][0][1] > null_threshold_cnt:
            print(f"\tNull threshold is {null_threshold_cnt}")
            print(f"\tCount missing from station {resp['smry'][0][1]}")
            return None
        if resp == {}:
            print("No data.")
            return None

        return resp

    # collect data from that station
    def retrieve_station_data_gdu(
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
            "elems": "1,2",
        }

        resp = requests.post(
            self.url_station_collect,
            data={"params": json.dumps(params)},
            headers={"Accept": "application/json"},
        )
        try:
            resp = resp.json()
        except:
            print("Error converting result to json")
            print(resp.text)

        cnt_missing = 0
        for datum in resp["data"]:
            try:
                datum.index("M")
                cnt_missing += 1
            except ValueError:
                continue

        if cnt_missing > null_threshold_cnt + 2:
            print(f"\tNull threshold is {null_threshold_cnt}")
            print(f"\tCount missing from station {cnt_missing}")
            return None

        if resp == {}:
            print("No data.")
            return None

        return resp

    def calc_cum_precip(self, start_date, end_date, lon, lat):
        """Get cumulative precipitation
        Based on hourly data"""
        # get df of distance to all stations
        logging.info("Calculating distance from point to all stations")
        self.sorted_list_stations_pcpn = self.get_dist_to_stations(
            self.list_stations_pcpn, lon, lat
        )
        attempt = 0
        while True:
            logging.info(f"Attempt no. {attempt}")
            closest_station = self.sorted_list_stations_pcpn[attempt]
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

    def calc_gdu(self, start_date, end_date, lon, lat):
        """Get gdu daily data"""
        """test
        start_date = '2024-08-05'
        end_date = '2024-10-25'
        lon = -92.61638
        lat = 45.23695
        """
        logging.info("Calculating distance from point to all stations")
        self.sorted_list_stations_gdu = self.get_dist_to_stations(
            self.list_stations_gdu, lon, lat
        )
        attempt = 0
        while True:
            logging.info(f"Attempt no. {attempt}")
            closest_station = self.sorted_list_stations_gdu[attempt]
            stationid = closest_station["sids"][0]
            distance = closest_station["distance"]
            logging.info(f"Pulling data from: {stationid}")
            logging.info(f"Distance away: {distance} km")

            nearest_station_data = self.retrieve_station_data_gdu(
                stationid, start_date, end_date
            )

            if nearest_station_data is None:
                logging.info("No data found.")
                attempt += 1
            else:
                break

        gdu = self.gdu_be(nearest_station_data)

        # gdu = nearest_station_data["smry"][0][0]
        # Result object to return
        result = {
            "dist_to_station_km": closest_station["distance"],
            "stationid": stationid,
            "gdu": gdu,
            "start_date": start_date,
            "end_date": end_date,
        }

        return result

    def get_weather_data(self, start_date, end_date, lon, lat, target="pcpn"):
        """if target = pcpn then cumulative precip
        else target = gdu then GDU
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

        if target == "pcpn":
            result = self.calc_cum_precip(start_date, end_date, lon, lat)
        elif target == "gdu":
            result = self.calc_gdu(start_date, end_date, lon, lat)

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


def gather_gdu_precip_2023plus(seasons=["fall"], mode="if_missing"):

    # If survey year is before 2023 then we skip and handle elsewhere.
    # These years had poorly formed dates.
    retrieve_acis = RetrieveACIS()

    survey_fields = SurveyField.objects.filter(survey_farm__survey_year__gt=2022)

    for survey_field in survey_fields:

        print(survey_field.survey_farm.id)
        for season in seasons:
            print(f"\t{season}")
            grab_and_update_weather_dat(survey_field, retrieve_acis, season, mode=mode)


def grab_and_update_weather_dat(
    survey_field_instance, retrieve_acis, season="fall", mode="if_missing"
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
        precip_field_name = "total_precip"
        gdu_field_name = "acc_gdd"
    else:
        cc_collection = ancillary_data.spring_biomass_collection_date
        precip_field_name = "spring_total_precip"
        gdu_field_name = "spring_acc_gdd"

    try:

        field_location = (
            FieldFarm.objects.filter(id=survey_field_instance.field_farm_id)
            .first()
            .field_location
        )
    except:
        logging.error(
            f"No field farm record for survey field {survey_field_instance.id}"
        )
        return None

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

    if datetime.datetime.strptime(cc_planting_date, "%Y-%m-%d").date() > cc_collection:
        print("Planting date is AFTER collection date.")
        return None

    if (
        getattr(ancillary_data, precip_field_name) is None and mode == "if_missing"
    ) or mode != "if_missing":
        result = retrieve_acis.get_weather_data(
            start_date, end_date, lon, lat, target="pcpn"
        )
        setattr(ancillary_data, precip_field_name, float(result["cumulative_precip"]))

    if (
        getattr(ancillary_data, gdu_field_name) is None and mode == "if_missing"
    ) or mode != "if_missing":
        result = retrieve_acis.get_weather_data(
            start_date, end_date, lon, lat, target="gdu"
        )
        setattr(ancillary_data, gdu_field_name, float(result["gdu"]))

    ancillary_data.save()


def update_gdu_precip_2020_2022():
    from django.db import connection

    retrieve_acis = RetrieveACIS()

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

        # calc precip
        total_precip = retrieve_acis.get_weather_data(
            start_date, end_date, lon, lat, target="pcpn"
        )["cumulative_precip"]
        # calc gdu
        gdu = retrieve_acis.get_weather_data(
            start_date, end_date, lon, lat, target="gdu"
        )["gdu"]

        print("Old => new")
        print(f"{old_precip} => {total_precip}")
        print(f"{old_gdu} => {gdu}")
        # update
        update_static_record(static_id, "total_precip", total_precip)
        update_static_record(static_id, "acc_gdd", gdu)


def weather_data():
    """For updating weather data
    update_null_precip - update precip where it is null
    update_null_gdu - update gud where it is null
    update_all_precip - update all precip
    update_all_gdu - update all gdu
    """
