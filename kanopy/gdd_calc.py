# Question about growing degree days:
# when do I start calculating? Beginning in the spring? Or if it's fall planted do I go b


import requests
import geopandas

# import matplotlib.pyplot as plt
# from shapely import wkt
from shapely.geometry import Point

# scratch
# python manage.py shell
# from kanopy.models import Groundcoverdoc

# docs = Groundcoverdoc.objects.all()
# doc = docs[0]


# Look up stations


def get_stations():

    states = ["MN", "SD", "ND", "IA", "WI"]
    url_station_collect = "https://cli-dap.mrcc.purdue.edu/state/{state}/"
    headers = {"Accept": "application/json"}

    list_stations = []
    for state in states:
        resp = requests.get(url_station_collect.format(state=state), headers=headers)
        resp = resp.json()
        list_stations.extend(resp)

    # convert to geospatial
    df_stations = geopandas.pd.DataFrame(list_stations)
    df_stations = geopandas.GeoDataFrame(
        df_stations,
        geometry=geopandas.points_from_xy(
            df_stations.stationlongitude, df_stations.stationlatitude
        ),
        crs=4326,
    )

    return df_stations


# find nearest station to covercrop location
def find_nearest_station(df_stations, df_collection):

    df_stations = df_stations.to_crs(epsg=5070)

    ## duplication records in collection to work with
    ##  distance function
    dupe_collection = df_collection.copy()
    for i in range(1, len(df_stations)):
        dupe_collection = geopandas.pd.concat([dupe_collection, df_collection])
    dupe_collection = dupe_collection.to_crs(epsg=5070)

    dupe_collection.reset_index(inplace=True, drop=True)
    dist = dupe_collection.distance(df_stations, align=True)
    dist.name = "distance"
    df_station_distance = df_stations.join(dist)
    df_station_distance.sort_values("distance", inplace=True)
    # idx_closest_station = dist.idxmin()
    # closest_station = df_stations.iloc[ idx_closest_station ]

    # return closest_station
    return df_station_distance


# collect data from that station


def retrieve_station_data(stationid, start_date, end_date):

    interval = "dly"
    element = "AVA"
    reductions = "&reduction=".join(["max", "min", "avg"])

    url_station_collect = (
        "https://cli-dap.mrcc.purdue.edu/station/{stationid}/data?{query_string}"
    )
    headers = {"Accept": "application/json"}

    payload = "start={start_date}&end={end_date}&elem={element}&interval={interval}&reduction={reduction}".format(
        start_date=start_date,
        end_date=end_date,
        element=element,
        interval=interval,
        reduction=reductions,
    )
    payload = "start={start_date}&end={end_date}&elem={element}".format(
        start_date=start_date,
        end_date=end_date,
        element=element,
    )

    resp = requests.get(
        url_station_collect.format(stationid=stationid, query_string=payload),
        headers=headers,
    )
    resp = resp.json()
    if resp == {}:
        print("No data.")
        return None
    df = geopandas.pd.DataFrame(resp).transpose()

    df.AVA = geopandas.pd.to_numeric(df.AVA, errors="coerce")

    prop_missing = df.AVA.isna().sum() / len(df)
    print(f"{round(prop_missing,3) *100} missing")

    if prop_missing > 0.05:
        return None

    df["collect_time"] = geopandas.pd.to_datetime(df.index, format="%Y%m%d%H%M")

    grpd = df.groupby(geopandas.pd.Grouper(key="collect_time", axis=0, freq="D")).agg(
        min_temp=geopandas.pd.NamedAgg(column="AVA", aggfunc="min"),
        max_temp=geopandas.pd.NamedAgg(column="AVA", aggfunc="max"),
        avg_temp=geopandas.pd.NamedAgg(column="AVA", aggfunc="mean"),
        count_obs=geopandas.pd.NamedAgg(column="AVA", aggfunc="count"),
    )

    return grpd


# QA/QC,

# Calculate growing degree days


def calc_gdd(doc, base_number=40, upper_thresh=86):

    # Verify planting date is before photo date
    if doc.photo_taken_date <= doc.cover_crop_planting_date:
        return None

    df_collection = geopandas.GeoDataFrame(
        {
            "photo_taken_date": [doc.photo_taken_date],
            "cover_crop_planting_date": [doc.cover_crop_planting_date],
            "geometry": [Point(doc.collectionpoint.coords)],
        },
        crs=4326,
    )

    # gets all stations
    df_stations = get_stations()

    # get df of distance to all stations
    df_station_distance = find_nearest_station(df_stations, df_collection)

    attempt = 0
    while True:

        closest_station = df_station_distance.iloc[attempt]
        stationid = closest_station.weabaseid

        df_station_data = retrieve_station_data(
            stationid,
            doc.cover_crop_planting_date.strftime("%Y%m%d"),
            doc.photo_taken_date.strftime("%Y%m%d"),
        )

        if df_station_data is None:
            attempt += 1
        else:
            break

    # If greater than 86, set to 86
    df_station_data.avg_temp = df_station_data.avg_temp.where(
        df_station_data.avg_temp < 86, 86
    )

    gdd = df_station_data.avg_temp - base_number

    # Where greater or equal to 0 keep; otherwise replace with 0
    gdd.where(gdd >= 0, 0, inplace=True)

    cumulative_gdd = gdd.sum()

    return cumulative_gdd
