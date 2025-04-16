import re
import pandas as pd
from django.contrib.auth.models import User
from wisccc.models import AncillaryData, SurveyFarm, SurveyField, Farmer
import datetime

fl_dairyland = "./data/labdata_2024/DAN_MARZU_2025-01-08 Dairyland report.csv"
fl_agsource = "./data/labdata_2024/SF07350-000 CC.CSV"

pattern = "(\d{4,5}-\d{2}-[FfS])"

dairyland = pd.read_csv(fl_dairyland)


def clean_nan(row):
    target_vars = [
        "CP",
        "aNDF",
        "uNDFom30",
        "NDFD30",
        "TDN_ADF",
        "Milk/Ton_Milk2013",
        "RFQ",
        "RFV",
        "uNDFom240",
        "Dry_Matter",
        "Total Nitrogen",
        "Biomass Dry",
    ]

    for targ in target_vars:
        if targ not in list(row.index):
            continue
        if pd.isna(row[targ]):
            row[targ] = None

    return row


def populate_ancil_record_dl(row, survey_field):
    # If none then add the date for collection
    # Create ancillarydata record if none exists
    try:
        ancillarydata = AncillaryData.objects.get(survey_field=survey_field)
    except:
        ancillarydata = AncillaryData.objects.create(survey_field=survey_field)

    farmer_last_name = ancillarydata.survey_field.survey_farm.farmer.last_name
    farmer_first_name = ancillarydata.survey_field.survey_farm.farmer.first_name
    check_url = f"https://evansgeospatial.com/update_labdata/{ancillarydata.survey_field.survey_farm.id}"

    print(f"\tDairyland: {farmer_first_name} {farmer_last_name}: {check_url}")
    if ancillarydata.biomass_collection_date is None:
        ancillarydata.biomass_collection_date = pd.to_datetime(row["Date_Processed"])
    # If current date is LATER than this collection date, replace with earlier
    elif pd.to_datetime(ancillarydata.biomass_collection_date) > pd.to_datetime(
        row["Date_Processed"]
    ):
        ancillarydata.biomass_collection_date = pd.to_datetime(row["Date_Processed"])
    ancillarydata.cp = row["CP"]
    ancillarydata.andf = row["aNDF"]
    ancillarydata.undfom30 = row["uNDFom30"]
    ancillarydata.ndfd30 = row["NDFD30"]
    ancillarydata.tdn_adf = row["TDN_ADF"]
    ancillarydata.milk_ton_milk2013 = row["Milk/Ton_Milk2013"]
    ancillarydata.rfq = row["RFQ"]
    ancillarydata.rfv = row["RFV"]
    ancillarydata.undfom240 = row["uNDFom240"]
    # ancillarydata.dry_matter = row["Dry_Matter"]

    print(f"\tDM Before: {ancillarydata.dry_matter}")
    ancillarydata.dry_matter = row["Dry_Matter"]
    print(f"\tDM After: {ancillarydata.dry_matter}")
    ancillarydata.save()


def populate_ancil_record_as(row, ancillarydata):
    # If none then add the date for collection
    farmer_last_name = ancillarydata.survey_field.survey_farm.farmer.last_name
    farmer_first_name = ancillarydata.survey_field.survey_farm.farmer.first_name
    check_url = f"https://evansgeospatial.com/update_labdata/{ancillarydata.survey_field.survey_farm.id}"

    print(f"\tAg source: {farmer_first_name} {farmer_last_name}: {check_url}")
    if ancillarydata.biomass_collection_date is None:
        ancillarydata.biomass_collection_date = pd.to_datetime(row["DATE Reported"])
    # If current date is LATER than this collection date, replace with earlier
    elif pd.to_datetime(ancillarydata.biomass_collection_date) > pd.to_datetime(
        row["DATE Reported"]
    ):
        ancillarydata.biomass_collection_date = pd.to_datetime(row["DATE Reported"])
    print(f"\tTN Before: {ancillarydata.total_nitrogen}")
    ancillarydata.total_nitrogen = row["Total Nitrogen"]
    print(f"\tTN After: {ancillarydata.total_nitrogen}")
    ancillarydata.cc_biomass = row["Biomass Dry"]

    ancillarydata.c_to_n_ratio = row["C-N Ratio"]
    
    ancillarydata.percent_p = row["P"]
    ancillarydata.percent_k = row["K"]
    ancillarydata.percent_ca = row["Ca"]
    ancillarydata.percent_mg = row["Mg"]
    ancillarydata.percent_s = row["S"]
    # ancillarydata.n_content = row["nitrogen_lbs_acre"]
    ancillarydata.p_content = row["P2O5 Lbs/Acre"]
    ancillarydata.k_content = row["K2O Lbs/Acre"]
    ancillarydata.ca_content = row["Ca Lbs/Acre"]     
    ancillarydata.mg_content = row["Mg Lbs/Acre"]     
    ancillarydata.s_content = row["S Lbs/Acre"]
    ancillarydata.c_content = row["Carbon Lbs/Acre"]

    ancillarydata.save()


def find_survey_field(farmer):
    survey_farm = SurveyFarm.objects.filter(farmer=farmer, survey_year=2024)
    if len(survey_farm) == 0:
        print(f"\tNo survey found...")
        return None

    if len(survey_farm) > 1:
        print(f"\tMultiple farm surveys?...")
        # For Josh Kamps first field

        if survey_farm[1].id == 168:
            print("\tJosh Kamps, returning first field")
            survey_field = SurveyField.objects.get(id=168)
            return survey_field

        if survey_farm[0] in (170, 182):
            print("\tKirk Leach, return first field")
            survey_field = SurveyField.objects.get(id=170)
            return survey_field

    survey_farm = survey_farm[0]
    survey_field = SurveyField.objects.filter(survey_farm=survey_farm)
    if len(survey_field) == 0:
        print("\tNo fields found")
        return None

    if len(survey_field) > 1:
        print(f"\tFound too many fields: {len(survey_field)}")
        return None

    survey_field = survey_field[0]
    return survey_field


second_fields = {
    # Josh Kamps
    # Original Farmer id: 55
    # '00055-24-F',
    # Second field Farmer id: 85
    # "00085-24-F": "00055-24-F",
    # Kirk Leach’s two fields
    # Original Farmer ID 32
    # '00032-24-F',
    # Second field Farmer ID 90
    "00090-24-F": "00032-24-F",
}

id_exceptions = {
    # Wrong ID
    # globalrootmass@gmail.com
    # Tom Burlingham (00081)
    "00077-24-F": "00081-24-F",
    # hgholsteins@gmail.com
    # Chris
    # Conley (00028)
    "00078-24-F": "00028-24-F",
    # kmbrewer04@gmail.com
    # Kimberly
    # Brewer (00057)
    "00079-24-F": "00057-24-F",
    # tdnovak081269@gmail.com
    # Tom
    # Novak (00031)
    "00080-24-F": "00031-24-F",
    # Jerry daniels, (00050)
    "00045-24-F": "00050-24-F",
}
# def import_dairyland():


for i, row in dairyland.iterrows():
    row = clean_nan(row)
    descr = row["Description1"] + str(row["Description2"])
    if descr == "Small Grainsfresh cutting":
        descr = "00034-24-F"
    rslt = re.search(pattern, descr)
    if rslt:
        print(rslt.group())
    else:
        print(f"No match found: {descr}")

        continue

    sample_id = rslt.group()

    if sample_id in id_exceptions.keys():
        print(f"\tChanging ids, was {sample_id}")
        sample_id = id_exceptions[sample_id]
        print(f"\tto {sample_id}")

    # Josh Kamps 2nd field
    if sample_id == "00085-24-F":
        print("Josh kamps second field!")

        # survey_field = SurveyField.objects.get(id=171)
        # try:
        #     ancillarydata = AncillaryData.objects.get(survey_field=survey_field)
        # except:
        #     ancillarydata = AncillaryData.objects.create(survey_field=survey_field)

        # populate_ancil_record_dl(row, ancillarydata)
        continue

    farmer = Farmer.objects.get(id=int(sample_id.split("-")[0]))
    # if farmer.id == 55: break
    print(f"Survey for {farmer.first_name} {farmer.last_name}")

    survey_field = find_survey_field(farmer)
    if survey_field is None:
        print("\tError no survey field found.")
        rslt = input("Continue - Y, or Break - B\n")
        if rslt == "B":
            break
        else:
            continue
    print("")

    populate_ancil_record_dl(row, survey_field)

    print("-----------")

ags_farmers = []
agsource = pd.read_csv(fl_agsource)
for i, row in agsource.iterrows():
    row = clean_nan(row)
    descr = row["Grower Name"] + row["Client Sample ID"]
    print(descr)
    rslt = re.search(pattern, descr)
    if rslt:
        print(rslt.group())
        sample_id = rslt.group()
        if descr == "Dan MarzuRock Co 00055-24-f 1":
            print("Josh Kamps 1st field")
            # survey_field = SurveyField.objects.get(id=168)
            # try:
            #     ancillarydata = AncillaryData.objects.get(survey_field=survey_field)
            # except:
            #     ancillarydata = AncillaryData.objects.create(survey_field=survey_field)
            # populate_ancil_record_as(row, ancillarydata)
            continue
        elif descr == "Dan MarzuRock Co 00055-24-f 2":
            print("Josh Kamps 2nd field")

            # survey_field = SurveyField.objects.get(id=171)
            # try:
            #     ancillarydata = AncillaryData.objects.get(survey_field=survey_field)
            # except:
            #     ancillarydata = AncillaryData.objects.create(survey_field=survey_field)
            # populate_ancil_record_as(row, ancillarydata)
            continue
    else:

        if descr == "Dan MarzuJayne Ross":
            sample_id = "00021-24-F"
        elif descr == "Charles Born1":
            sample_id = "00083-24-F"
        elif descr == "Matthew Oehmichen1":
            sample_id = "00002-24-F"
        elif descr == "Skip Grosskreut1":
            sample_id = "00036-24-F"
        else:
            print(f"No match found: {descr}")
            continue

    if sample_id in id_exceptions.keys():
        # print(f"Changing ids, was {sample_id}")
        sample_id = id_exceptions[sample_id]
        # print(f"\tto {sample_id}")

    farmer = Farmer.objects.get(id=int(sample_id.split("-")[0]))
    print(f"Survey for {farmer.first_name} {farmer.last_name}")
    ags_farmers.append(f"{farmer.first_name} {farmer.last_name}")
    survey_field = find_survey_field(farmer)

    if survey_field is None:
        print("\tError no survey field found.")
        rslt = input("Continue - Y, or Break - B\n")
        if rslt == "B":
            break
        else:
            continue

    # Create ancillarydata record if none exists
    try:
        ancillarydata = AncillaryData.objects.get(survey_field=survey_field)
    except:
        ancillarydata = AncillaryData.objects.create(survey_field=survey_field)

    populate_ancil_record_as(row, ancillarydata)


for dl in dl_farmers:
    if dl not in ags_farmers:
        print(f"{dl} not in Ag Source")

for ags in ags_farmers:
    if ags not in dl_farmers:
        print(f"{ags} not in Dairyland")


## Checking

import re
import pandas as pd
from django.contrib.auth.models import User
from wisccc.models import AncillaryData, SurveyFarm, SurveyField, Farmer
import datetime

fl_dairyland = "./data/labdata_2024/DAN_MARZU_2025-01-08 Dairyland report.csv"
fl_agsource = "./data/labdata_2024/SF07350-000 CC.CSV"
fl_downloaded_data = "../../Downloads/full_survey_questions(12).csv"
pattern = "(\d{4,5}-\d{2}-[FfS])"

prod_data = pd.read_csv(fl_downloaded_data)
dairyland = pd.read_csv(fl_dairyland)
agsource = pd.read_csv(fl_agsource)

for i, row in dairyland.iterrows():

    # descr = row["Grower Name"] + row["Client Sample ID"]
    descr = row["Description1"] + str(row["Description2"])
    # print(descr)
    rslt = re.search(pattern, descr)
    sample_id = rslt.group()
    if sample_id in id_exceptions.keys():
        # print(f"Changing ids, was {sample_id}")
        sample_id = id_exceptions[sample_id]

    print(f"Survey for {farmer.first_name} {farmer.last_name}")
