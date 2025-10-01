import pandas as pd
import numpy as np
import geopandas
import os

from django.contrib.gis.geos import GEOSGeometry, Point

from glccp.models import CleanedData



def create_models_doc():
    overwrite = True
    model_doc = "./models.py"
    if os.path.exists(model_doc):
        rslt = input("Are you sure you want to overwrite the existing model doc?\n")
        if rslt.lower() != "y" and rslt.lower() != "yes":
            2 / 0

    dat = pd.read_excel(fl_data)
    dat = dat.rename(columns={"%Cover": "percent_cover"})
    dat.columns = dat.columns.str.lower()

    float_field = """\t{col} = models.DecimalField(decimal_places=2, max_digits=15, verbose_name="", null=True)\n"""
    text_field = (
        """\t{col} = models.CharField(verbose_name="", null=True, max_length=250)\n"""
    )
    int_field = """\t{col} = models.IntegerField(verbose_name="", null=True)\n"""
    date_field = """\t{col} = models.DateField(null=True)\n"""

    with open(model_doc, "wt") as doc:

        doc.write("from django.db import models\n")
        doc.write("from django.contrib.gis.db import models as geo_models\n\n")

        doc.write("class CleanedData(models.Model):\n\n")
        for col in dat.columns:
            thetype = dat[col].dtype
            print(f"{col}: {thetype}")
            if str(thetype) == "float64":
                field_line = float_field.format(col=col)
            if str(thetype) == "object":
                field_line = text_field.format(col=col)
            if str(thetype) == "datetime64[ns]":
                field_line = date_field.format(col=col)
            if str(thetype) == "int64":
                field_line = int_field.format(col=col)

            doc.write(field_line)

        doc.write(
            """\tfarm_location = geo_models.PointField(verbose_name="Location", null=True)\n\n"""
        )


def find_lat_long(zipcode, zipcodes):

    target_zip = zipcodes.loc[zipcodes.ZCTA5CE20 == str(zipcode)]
    if len(target_zip) == 0:
        return None
    centroid = target_zip.centroid.reindex().iloc[0]
    sigma = 0.045
    longitude = centroid.x + np.random.uniform(-sigma, sigma, 1)[0]
    latitude = centroid.y + np.random.uniform(-sigma, sigma, 1)[0]

    pt = GEOSGeometry(f"POINT({longitude} {latitude})")
    pt.srid = 4269
    return pt  # f"POINT({longitude} {latitude})"


def makeFarmLocationFile():
    '''Because the zip code file can't be 
    used on the remote server we need to create a file
    of farm locations which can be joined on.'''
    fl_data = "~/Documents/exploring_soils/data/GLCCP_2024-2025_interactive map_data_v3.xlsx"
    fl_zipcodes = "/home/evans/Documents/small_projects/wisc_cc/tl_2020_us_zcta520/tl_2020_us_zcta520.shp"
    zipcodes = geopandas.read_file(
        fl_zipcodes
        # bbox=(-96.42389620756555, 37.18015493447337, -81.83489159751977, 45.94466927653207),
    )
    # fl_data = "/home/ubuntu/GLCCP_2024-2025_interactive map_data_v3.xlsx"
    year = "2025"
    fl_loc = "farm_locations_2025.csv"
    fl_nozip = "nozip_2025.csv"
    # fl_zipcodes = "/home/ubuntu/tl_2020_us_zcta520.shp"
    with open(fl_loc, "wt") as f:
        f.write("farm\tfield\tyear\tfarm_location\n")
    with open(fl_nozip, "wt") as f:
        f.write("farm\tfield\tyear\tzipcode\n")        

    dat = pd.read_excel(fl_data)
    dat.columns = dat.columns.str.lower()
    for i, row in dat.iterrows():
        farm_id = row["farm"]
        field_id = row["field"]
        zipcode = row['zipcode']
        if "-" in zipcode:
            
            zipcode = zipcode[:5]

        print(f"Farm field: {farm_id} {field_id}:")
        pt = find_lat_long(zipcode, zipcodes)
        try:
            with open(fl_loc, "at") as f:
                f.write(f"{farm_id}\t{field_id}\t{year}\t{pt.wkt}\n")
            print("\tFound zip.")
        except AttributeError as e:
            with open(fl_nozip, "at") as f:
                f.write(f"{farm_id}\t{field_id}\t{year}\t{zipcode}\n")
            print("\tNo zip.")
        print("____________________")


def load2025():
    skip_cols = [
        "CC_current_grazecutmow",
        "CC_current_fieldprep",
        "CC-plantgreen",
        "How do you plan to terminate the cover crop? - Selected Choice",
        "CC_sampledate_year",
        "CC_sampledate_day",
        "CC_sampledate_month.1",
        "CC_sampledate_month",
        "CC_plantdate_year",
        "CC_plantdate_day",
        "CC_plantdate_month",
        "How would you describe soil moisture during the first two weeks after cover crop planting?",
        "Was the cover crop planted before, during or after harvest of your cash crop?",
        "CC_current_var",
        "CC_sampledate_day_s",
        "CC_plantdate_day_s"
        ]

    

    fl_data = "/home/ubuntu/exploring_soils/data/GLCCP_2024-2025_interactive map_data_v3.xlsx"
    fl_loc = "/home/ubuntu/exploring_soils/data/farm_locations_2025.csv"
    fl_data = "~/Documents/exploring_soils/data/GLCCP_2024-2025_interactive map_data_v3.xlsx"
    fl_loc = "~/Documents/exploring_soils/farm_locations_2025.csv"
    # fl_zipcodes = "/home/ubuntu/tl_2020_us_zcta520.shp"
    # fl_zipcodes = "/home/evans/Documents/small_projects/wisc_cc/tl_2020_us_zcta520/tl_2020_us_zcta520.shp"
    # zipcodes = geopandas.read_file(
    #     fl_zipcodes
    #     # bbox=(-96.42389620756555, 37.18015493447337, -81.83489159751977, 45.94466927653207),
    # )
    

    dat = pd.read_excel(fl_data)
    dat.CC_plantdate_year = dat.CC_plantdate_year.astype("string").str[:4]
    dat.CC_plantdate_month = dat.CC_plantdate_month.astype("string")
    dat["CC_plantdate_day_s"] = dat.CC_plantdate_day.astype("string")

    dat.CC_sampledate_year = dat.CC_sampledate_year.astype("string").str[:4]
    dat.CC_sampledate_month = dat.CC_sampledate_month.astype("string")
    dat["CC_sampledate_day_s"] = dat.CC_sampledate_day.astype("string")    
    
    dat['year'] = 2025

    # , format="%Y-%B-%d")
    dat['cc_plantdate'] = pd.to_datetime(
        dat['CC_plantdate_year'] + dat['CC_plantdate_month'] + dat['CC_plantdate_day_s'], 
        format="%Y%B%d"
    )
    dat['cc_sampledate'] = pd.to_datetime(
        dat['CC_sampledate_year'] + dat['CC_sampledate_month.1'] + dat['CC_sampledate_day_s'], 
        format="%Y%B%d"
    )    
    
    dat = dat.drop(columns=skip_cols)
    dat = dat.rename(
        columns={
            "%Cover": "percent_cover",
            "Tillage_intensity_norm": "Tillage_intensity_norm_V2",
            "CC_current_overwinter_richness": "richness"
            }
        )
    dat.columns = dat.columns.str.lower()
    no_location = []
    loc = pd.read_csv(fl_loc, sep="\t")
    
    dat = dat.join(loc.set_index(["farm", "field", "year"]), on=["farm", "field", "year"])


    for i, row in dat.iterrows():

        farm_id = row["farm"]
        field_id = row["field"]
        print(f"Farm field: {farm_id} {field_id}:")
        
        cleaned_data_record = CleanedData.objects.create()

        dict_row = row.to_dict()
        for field, value in dict_row.items():

            if pd.isna(value):
                value = None
            # For remote
            if field == "farm_location":
                print(f"\tFarm location: {value}")
                if value is not None:
                    pt = GEOSGeometry(value)
                    pt.srid = 4269
                    print(f"\tpt: {pt}")
                    setattr(cleaned_data_record, field, pt)
            else:
                setattr(cleaned_data_record, field, value)
            cleaned_data_record.save()
            # For local
            # farm_location = find_lat_long(row.zipcode, zipcodes)
            # if farm_location is None:
            #     no_location.append(row)
            # setattr(cleaned_data_record, field, value)
            # cleaned_data_record.farm_location = GEOSGeometry(farm_location)
            # cleaned_data_record.save()


def checkout2025():
    fl_data = "/home/ubuntu/exploring_soils/data/GLCCP_2024-2025_interactive map_data_v3.xlsx"
    fl_loc = "/home/ubuntu/exploring_soils/data/farm_locations_2025.csv"
    fl_data = "~/Documents/exploring_soils/data/GLCCP_2024-2025_interactive map_data_v3.xlsx"
    fl_loc = "~/Documents/exploring_soils/farm_locations_2025.csv"
    dat = pd.read_excel(fl_data)

    glccp_2025 = CleanedData.objects.filter(year=2025)

    db_count = glccp_2025.count()
    fl_count = len(dat)

    try:
        assert(db_count == fl_count)
    except:
        print("The count of records in the DB differs from the file!")






def load2022and2023():
    fl_data = "~/Documents/glccp/Interactive Map_data_v2.xlsx"
    fl_zipcodes = "/home/evans/Documents/small_projects/wisc_cc/tl_2020_us_zcta520/tl_2020_us_zcta520.shp"

    fl_data = "/home/ubuntu/Interactive Map_data_v2.xlsx"
    fl_loc = "/home/ubuntu/farm_locations.csv"
    # fl_zipcodes = "/home/ubuntu/tl_2020_us_zcta520.shp"

    zipcodes = geopandas.read_file(
        fl_zipcodes
        # bbox=(-96.42389620756555, 37.18015493447337, -81.83489159751977, 45.94466927653207),
    )

    dat = pd.read_excel(fl_data)
    dat = dat.rename(columns={"%Cover": "percent_cover"})
    dat.columns = dat.columns.str.lower()
    no_location = []
    loc = pd.read_csv(fl_loc)
    dat = dat.merge(loc, on=["farm", "field", "year"])


    for i, row in dat.iterrows():

        farm_id = row["farm"]
        field_id = row["field"]
        print(f"Farm field: {farm_id} {field_id}:")
        cleaned_data_record = CleanedData.objects.create()

        dict_row = row.to_dict()
        for field, value in dict_row.items():


            if pd.isna(value):
                value = None
            # For local
            # farm_location = find_lat_long(row.zipcode, zipcodes)
            # if farm_location is None:
            #     no_location.append(row)
            # setattr(cleaned_data_record, field, value)
            # cleaned_data_record.farm_location = GEOSGeometry(farm_location)
            # cleaned_data_record.save()

            # For remote
            if field == "farm_location":
                print(f"\tFarm location: {value}")
                if value is not None:
                    pt = GEOSGeometry(value)
                    pt.srid = 4269
                    print(f"\tpt: {pt}")
                    setattr(cleaned_data_record, field, pt)
            else:
                setattr(cleaned_data_record, field, value)
            cleaned_data_record.save()


## Investigating differences in data versions

dat_v1 = pd.read_excel("~/Documents/glccp/Interactive Map_data.xlsx")
dat_v2 = pd.read_excel("~/Documents/glccp/Interactive Map_data_v2.xlsx")
dat_v3 = pd.read_excel("~/Documents/glccp/GLCCP_2024-2025_interactive map_data_v3.xlsx")

col_diffs = dat_v1 == dat_v2

for col in col_diffs:
    if col_diffs[col].sum() != 253:
        if col in ["CC_sampledate", "CC_plantdate"]:
            continue
        num_diffs = 253 - col_diffs[col].sum()
        print(f"{num_diffs} differences in {col}")
        print("\tVals in v1:")
        print("\t", dat_v1[col].loc[~col_diffs[col]])
        print("\tVals in v2:")
        print("\t", dat_v2[col].loc[~col_diffs[col]])
        rslt = input("Y to continue")
        if rslt != "y":
            break


    # for i, row in dat.iterrows():
    #     testdate = row['CC_sampledate_year'] + row['CC_sampledate_month.1'] +row['CC_sampledate_day_s']
    #     try:
    #         pd.to_datetime(testdate, format="%Y%B%d")
    #     except:
    #         print(row["Farm"], row["Field"])
    #         print("\t", row['CC_sampledate_year'], row['CC_sampledate_month.1'], row['CC_sampledate_day_s'])
    #         print("\tFailed to make date.")
    #         print("_______________________") 
    # testdate = row['CC_plantdate_year'] + row['CC_plantdate_month'] +row['CC_plantdate_day_s']
    # try:
    #     pd.to_datetime(testdate, format="%Y%B%d")
    # except:
    #     print(row["Farm"], row["Field"])
    #     print("\t", row['CC_plantdate_year'], row['CC_plantdate_month'], row['CC_plantdate_day_s'])
    #     print("\tFailed to make date.")
    #     print("_______________________")