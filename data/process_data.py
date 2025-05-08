import re
import pandas as pd
from django.contrib.auth.models import User
from wisccc.models import AncillaryData, SurveyFarm, SurveyField, Farmer
import datetime

'''For push data to server, from ./infra
pullip () {
    sed -e 's/^"//' -e 's/"$//' <<< $(terraform output ip)
}
ipaddress=$( pullip )
scp -i ~/.ssh/wieff_1.pem ../data/labdata_2023/all_lab_data_2023.tsv ubuntu@$ipaddress:~/.
scp -i ~/.ssh/wieff_1.pem ../data/labdata_2023/bn05905_p_cover_crop2023_biomass.csv ubuntu@$ipaddress:~/.
scp -i ~/.ssh/wieff_1.pem ../data/labdata_2023/spring_lab_data/BN5905\ UW\ COVER_CROP.CSV ubuntu@$ipaddress:~/.
scp -i ~/.ssh/wieff_1.pem ../data/labdata_2023/dairyland_labs_forage_analysis_data_2023.csv ubuntu@$ipaddress:~/.
scp -i ~/.ssh/wieff_1.pem ../data/labdata_2023/spring_lab_data/SHC\ 2023-2024\ Dairyland\ Labs\ data.csv ubuntu@$ipaddress:~/.
scp -i ~/.ssh/wieff_1.pem ../data/labdata_2024/DAN_MARZU_2025-01-08\ Dairyland\ report.csv ubuntu@$ipaddress:~/.
scp -i ~/.ssh/wieff_1.pem ../data/labdata_2024/SF07350-000\ CC.CSV ubuntu@$ipaddress:~/.
scp -i ~/.ssh/wieff_1.pem ../data/calcs_from_dan_marzu/23\ to\ 24\ weights\ and\ heights.xlsx ubuntu@$ipaddress:~/.

# on remote server
sudo mv *.csv ./exploring_soils/data/.
sudo mv *.CSV ./exploring_soils/data/.
sudo mv *.tsv ./exploring_soils/data/.
sudo mv *.xlsx ./exploring_soils/data/.
'''
# Cross walk between lab IDs and old survey_response_ids


fl_lkup = "./data/labdata_2023/all_lab_data_2023.tsv"
fl_lkup = "./data/all_lab_data_2023.tsv"

lkup = pd.read_csv(fl_lkup, sep="\t")

def populate_ancil_record_as_fall(row, ancillarydata):
    # If none then add the date for collection    
    if ancillarydata.biomass_collection_date is None:
        ancillarydata.biomass_collection_date = pd.to_datetime(row["DATE Reported"])
    # If current date is LATER than this collection date, replace with earlier
    elif pd.to_datetime(ancillarydata.biomass_collection_date) > pd.to_datetime(
        row["DATE Reported"]
    ):
        ancillarydata.biomass_collection_date = pd.to_datetime(row["DATE Reported"])
    
    ancillarydata.total_nitrogen = row["Total Nitrogen"]
    ancillarydata.cc_biomass = row["Biomass Dry"]
    ancillarydata.c_to_n_ratio = row["C-N Ratio"]
    ancillarydata.percent_p = row["P"]
    ancillarydata.percent_k = row["K"]
    ancillarydata.percent_ca = row["Ca"]
    ancillarydata.percent_mg = row["Mg"]
    ancillarydata.percent_s = row["S"]
    if row["Carbon Lbs/Acre"] is None or row["C-N Ratio"] is None:
        ancillarydata.n_content = None
    else:
        ancillarydata.n_content = row["Carbon Lbs/Acre"] / row["C-N Ratio"]
    ancillarydata.p_content = row["P2O5 Lbs/Acre"]
    ancillarydata.k_content = row["K2O Lbs/Acre"]
    ancillarydata.ca_content = row["Ca Lbs/Acre"]     
    ancillarydata.mg_content = row["Mg Lbs/Acre"]     
    ancillarydata.s_content = row["S Lbs/Acre"]
    ancillarydata.c_content = row["Carbon Lbs/Acre"]

    ancillarydata.save()

def populate_ancil_record_as_spring(row, ancillarydata):
    # If none then add the date for collection    
    if ancillarydata.spring_biomass_collection_date is None:
        ancillarydata.spring_biomass_collection_date = pd.to_datetime(row["DATE Reported"])
    # If current date is LATER than this collection date, replace with earlier
    elif pd.to_datetime(ancillarydata.spring_biomass_collection_date) > pd.to_datetime(
        row["DATE Reported"]
    ):
        ancillarydata.spring_biomass_collection_date = pd.to_datetime(row["DATE Reported"])
    
    ancillarydata.spring_total_nitrogen = row["Total Nitrogen"]
    ancillarydata.spring_cc_biomass = row["Biomass Dry"]
    ancillarydata.spring_c_to_n_ratio = row["C-N Ratio"]
    ancillarydata.spring_percent_p = row["P"]
    ancillarydata.spring_percent_k = row["K"]
    ancillarydata.spring_percent_ca = row["Ca"]
    ancillarydata.spring_percent_mg = row["Mg"]
    ancillarydata.spring_percent_s = row["S"]
    ancillarydata.spring_n_content = row["Carbon Lbs/Acre"] / row["C-N Ratio"]
    ancillarydata.spring_p_content = row["P2O5 Lbs/Acre"]
    ancillarydata.spring_k_content = row["K2O Lbs/Acre"]
    ancillarydata.spring_ca_content = row["Ca Lbs/Acre"]     
    ancillarydata.spring_mg_content = row["Mg Lbs/Acre"]     
    ancillarydata.spring_s_content = row["S Lbs/Acre"]
    ancillarydata.spring_c_content = row["Carbon Lbs/Acre"]

    ancillarydata.save()

def populate_ancil_record_dl_fall(row, ancillarydata):
    # If none then add the date for collection    
    if ancillarydata.biomass_collection_date is None:
        ancillarydata.biomass_collection_date = pd.to_datetime(row["Date_Processed"])
    # If current date is LATER than this collection date, replace with earlier
    elif pd.to_datetime(ancillarydata.biomass_collection_date) > pd.to_datetime(
        row["Date_Processed"]
    ):
        ancillarydata.biomass_collection_date = pd.to_datetime(row["Date_Processed"])
    

    ancillarydata.cp = row["CP"]
    ancillarydata.adf = row["ADF"]
    ancillarydata.andf = row["aNDF"]
    ancillarydata.undfom30 = row["uNDFom30"]
    ancillarydata.ndfd30 = row["NDFD30"]
    ancillarydata.tdn_adf = row["TDN_ADF"]
    ancillarydata.milk_ton_milk2013 = row["Milk/Ton_Milk2013"]
    ancillarydata.rfq = row["RFQ"]
    ancillarydata.undfom240 = row["uNDFom240"]
    ancillarydata.dry_matter = row["Dry_Matter"]
    ancillarydata.rfv = row["RFV"]

    ancillarydata.save()

def populate_ancil_record_dl_spring(row, ancillarydata):
    # If none then add the date for collection    
    if ancillarydata.spring_biomass_collection_date is None:
        ancillarydata.spring_biomass_collection_date = pd.to_datetime(row["Date Processed"])
    # If current date is LATER than this collection date, replace with earlier
    elif pd.to_datetime(ancillarydata.spring_biomass_collection_date) > pd.to_datetime(
        row["Date Processed"]
    ):
        ancillarydata.spring_biomass_collection_date = pd.to_datetime(row["Date Processed"])
    

    ancillarydata.spring_cp = row["CP"]
    ancillarydata.spring_adf = row["ADF"]
    ancillarydata.spring_andf = row["aNDF"]
    ancillarydata.spring_undfom30 = row["uNDFom30"]
    ancillarydata.spring_ndfd30 = row["NDFD30"]
    ancillarydata.spring_tdn_adf = row["TDN - ADF"]
    ancillarydata.spring_milk_ton_milk2013 = row["Milk Per Ton - Milk 13"]
    ancillarydata.spring_rfq = row["RFQ"]
    ancillarydata.spring_undfom240 = row["uNDFom240"]
    ancillarydata.spring_dry_matter = row["Dry Matter"]
    ancillarydata.spring_rfv = row["RFV"]

    ancillarydata.save()


def process_agsource_fall_2023():
    fl_agsource_fall_23 = "./data/labdata_2023/bn05905_p_cover_crop2023_biomass.csv"
    fl_agsource_fall_23 = "./data/bn05905_p_cover_crop2023_biomass.csv"
    agsource_fall_23 = pd.read_csv(fl_agsource_fall_23)
    for i, row in agsource_fall_23.iterrows():
        
        lkup_match = lkup.loc[lkup.grower_name == row['Grower Name']]
        if len(lkup_match) == 0:
            print("No match found.")
            continue
        lkup_match = lkup_match.to_dict('records')[0]
        first_name = lkup_match["first_name"]
        last_name = lkup_match["last_name"]
        survey_response_id = lkup_match["id"]

        # John Goodman troubling weirdness
        if survey_response_id == 49:
            ancillary_data = AncillaryData.objects.get(survey_field_id=42)
        else:
            ancillary_data = AncillaryData.objects.get(
                survey_response_id=survey_response_id
            )
        
        farmer_last_name = ancillary_data.survey_field.survey_farm.farmer.last_name
        farmer_first_name = ancillary_data.survey_field.survey_farm.farmer.first_name
        print(f"Survey for {farmer_first_name} {farmer_last_name}")
        print(f"{first_name} {last_name}")
        
        populate_ancil_record_as_fall(row, ancillary_data)

def process_agsource_spring_2023():
    fl_agsource_spring_23 = "./data/labdata_2023/spring_lab_data/BN5905 UW COVER_CROP.CSV"
    fl_agsource_spring_23 = "./data/BN5905 UW COVER_CROP.CSV"
    agsource_spring_23 = pd.read_csv(fl_agsource_spring_23)
    for i, row in agsource_spring_23.iterrows():
        # print(f"{i}: {row['Grower Name']}")
        lkup_match = lkup.loc[lkup.grower_name_spring == row['Grower Name']]
        if len(lkup_match) == 0:
            print("No match found.")
            continue
        lkup_match = lkup_match.to_dict('records')[0]
        first_name = lkup_match["first_name"]
        last_name = lkup_match["last_name"]
        survey_response_id = lkup_match["id"]

        # Travis Klinker?
        # if survey_response_id == 59:
        #     print(f"{first_name} {last_name}")
        #     print("Travis Klinker")
        #     continue
        # John Goodman troubling weirdness
        if survey_response_id == 49:
            ancillary_data = AncillaryData.objects.get(survey_field_id=42)
        else:
            ancillary_data = AncillaryData.objects.get(
                survey_response_id=survey_response_id
            )
        
        farmer_last_name = ancillary_data.survey_field.survey_farm.farmer.last_name
        farmer_first_name = ancillary_data.survey_field.survey_farm.farmer.first_name
        print(f"Survey for {farmer_first_name} {farmer_last_name}")
        print(f"{first_name} {last_name}")
        
        populate_ancil_record_as_spring(row, ancillary_data)

def process_dairyland_fall_2023():
    fl_dairyland_fall_23 = (
        "./data/labdata_2023/dairyland_labs_forage_analysis_data_2023.csv"
    )
    fl_dairyland_fall_23 = "./data/dairyland_labs_forage_analysis_data_2023.csv"
    dairyland_fall_23 = pd.read_csv(fl_dairyland_fall_23)
    for i, row in dairyland_fall_23.iterrows():
        # print(f"{i}: {row['Grower Name']}")
        lkup_match = lkup.loc[lkup.description1 == row['Description1']]
        if len(lkup_match) == 0:
            print("No match found.")
            continue
        lkup_match = lkup_match.to_dict('records')[0]
        first_name = lkup_match["first_name"]
        last_name = lkup_match["last_name"]
        survey_response_id = lkup_match["id"]

        if survey_response_id == 49:
            ancillary_data = AncillaryData.objects.get(survey_field_id=42)
        else:
            ancillary_data = AncillaryData.objects.get(
                survey_response_id=survey_response_id
            )
        
        farmer_last_name = ancillary_data.survey_field.survey_farm.farmer.last_name
        farmer_first_name = ancillary_data.survey_field.survey_farm.farmer.first_name
        print(f"Data for {farmer_first_name} {farmer_last_name}")
        print(f"{first_name} {last_name}")
        row = clean_nan(row)
        populate_ancil_record_dl_fall(row, ancillary_data)

def process_dairyland_spring_2023():
    fl_dairyland_spring_23 = (
    "./data/SHC 2023-2024 Dairyland Labs data.csv"
    )
    dairyland_spring_23 = pd.read_csv(fl_dairyland_spring_23)
    for i, row in dairyland_spring_23.iterrows():
        # print(f"{i}: {row['Grower Name']}")
        lkup_match = lkup.loc[lkup.description1_spring == row['Description 1']]
        if len(lkup_match) == 0:
            print("No match found.")
            continue
        lkup_match = lkup_match.to_dict('records')[0]
        first_name = lkup_match["first_name"]
        last_name = lkup_match["last_name"]
        survey_response_id = lkup_match["id"]

        if survey_response_id == 49:
            ancillary_data = AncillaryData.objects.get(survey_field_id=42)
        else:
            ancillary_data = AncillaryData.objects.get(
                survey_response_id=survey_response_id
            )
        
        farmer_last_name = ancillary_data.survey_field.survey_farm.farmer.last_name
        farmer_first_name = ancillary_data.survey_field.survey_farm.farmer.first_name
        print(f"Data for {farmer_first_name} {farmer_last_name}")
        print(f"{first_name} {last_name}")

        populate_ancil_record_dl_spring(row, ancillary_data)        



def clean_nan(row):
    target_vars = [
        "CP",
        "ADF",
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
        "C-N Ratio",
        "P",
        "K",
        "Ca",
        "Mg",
        "S",
        "P2O5 Lbs/Acre",
        "K2O Lbs/Acre",
        "Ca Lbs/Acre",     
        "Mg Lbs/Acre",
        "S Lbs/Acre",
        "Carbon Lbs/Acre"
    ]

    for targ in target_vars:
        if targ not in list(row.index):
            continue
        if pd.isna(row[targ]):
            row[targ] = None

    return row


def find_survey_field(farmer, id_farmer=None):

    survey_farm = SurveyFarm.objects.filter(farmer=farmer, survey_year=2024)
    if len(survey_farm) == 0:
        print(f"\tNo survey found...")
        return None

    if len(survey_farm) > 1:
        print(f"\tMultiple farm surveys?...")
        return None

    survey_farm = survey_farm[0]
    
    survey_field = SurveyField.objects.filter(survey_farm=survey_farm)
    if len(survey_field) == 0:
        print("\tNo fields found")
        return None

    if len(survey_field) > 1:
        # Josh kamps second field
        if id_farmer == 85:
            survey_field = SurveyField.objects.get(id = 171)
        elif id_farmer == 55:
            survey_field = SurveyField.objects.get(id = 168)
        else:
            return None
        
        return survey_field

    survey_field = survey_field[0]
    return survey_field
        # if survey_farm[1].id == 168:
        #     print("\tJosh Kamps, returning first field")
        #     survey_field = SurveyField.objects.get(id=168)
        #     return survey_field

        # if survey_farm[0] in (170, 182):
        #     print("\tKirk Leach, return first field")
        #     survey_field = SurveyField.objects.get(id=170)
        #     return survey_field

def lookup_id_exceptions(clean_lab_id):
            

        id_exceptions = {
            # Wrong ID: right ID

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
        if clean_lab_id in id_exceptions.keys():
            print(f"\tChanging ids, was {clean_lab_id}")
            new_clean_lab_id = id_exceptions[clean_lab_id]
            print(f"\tto {new_clean_lab_id}")
            return new_clean_lab_id
        else:
            return clean_lab_id

def find_farmer(lab_id):
    '''For taking the description from Dairyland or Agsource,
    and returning the wisccc_farmer object'''
    # regex pattern for pulling out farmer id from lab id
    # Farmer id zero padded to five digits, hypen, 2 digit year, 
    # "F" for fall or "S" for spring
    #  ex 00034-24-F
    pattern = "(\d{4,5}-\d{2}-[FfS])"

    # Ron Schoep, lab screwup from Dairyland
    if lab_id == "Small Grainsfresh cutting":
        lab_id = "00034-24-F"
    # JK first field
    elif lab_id == "Dan MarzuRock Co 00055-24-f 1":
        lab_id = "00055-24-F"
    # JK second field assigned his second Farmer id to
    #   distinguish his second field
    elif lab_id == "Dan MarzuRock Co 00055-24-f 2":
        lab_id = "00085-24-F"
    elif lab_id == "Dan MarzuJayne Ross":
        lab_id = "00021-24-F"
    elif lab_id == "Charles Born1":
        lab_id = "00083-24-F"
    elif lab_id == "Matthew Oehmichen1":
        lab_id = "00002-24-F"
    elif lab_id == "Skip Grosskreut1":
        lab_id = "00036-24-F"

        
    rslt = re.search(pattern, lab_id)

    if rslt is None:
        
        print(f"No match found: {lab_id}")
        return None

    clean_lab_id = rslt.group()
    # Check to see if this is one of the id goof ups,
    #   and correct it
    clean_lab_id = lookup_id_exceptions(clean_lab_id)

    id_farmer = int(clean_lab_id.split("-")[0])
    print(f"{lab_id}\n{clean_lab_id}")

    return id_farmer



# No survey field found for kirk leach
def process_dairyland_fall_2024():
    fl_dairyland = "./data/labdata_2024/DAN_MARZU_2025-01-08 Dairyland report.csv"
    fl_dairyland = "./data/DAN_MARZU_2025-01-08 Dairyland report.csv"
    dairyland = pd.read_csv(fl_dairyland)
    for i, row in dairyland.iterrows():
        
        descr = row["Description1"] + str(row["Description2"])
        # print(descr)
        id_farmer = find_farmer(descr)
        if id_farmer is None:
            continue
        
        
        if id_farmer == 85:
            # JKs second field was given a different ID
            farmer = Farmer.objects.get(id=55)
        else:
            farmer = Farmer.objects.get(id=id_farmer)
        
        print(f"Survey for {farmer.first_name} {farmer.last_name}")
        
        survey_field = find_survey_field(farmer, id_farmer=id_farmer)
        if survey_field is None:
            print("\tError no survey field found.")
            rslt = input("Continue - Y, or Break - B\n")
            if rslt == "B":
                break
            else:
                continue

        print("")
        row = clean_nan(row)
        ancillary_data = AncillaryData.objects.get(
                survey_field_id=survey_field.id
            )
        populate_ancil_record_dl_fall(row, ancillary_data)

        print("-----------")    


def process_agsource_fall_2024():
    fl_agsource = "./data/labdata_2024/SF07350-000 CC.CSV"
    fl_agsource = "./data/SF07350-000 CC.CSV"
    agsource = pd.read_csv(fl_agsource)

    for i, row in agsource.iterrows():
        
        descr = row["Grower Name"] + row["Client Sample ID"]
        id_farmer = find_farmer(descr)

        if id_farmer is None:
            print("\tSkipping:")
            print(f"\t{descr}")
            continue
        elif id_farmer == 85:
            # JKs second field was given a different ID
            farmer = Farmer.objects.get(id=55)
        else:
            farmer = Farmer.objects.get(id=id_farmer)

        print(f"Survey for {farmer.first_name} {farmer.last_name}")
        
        survey_field = find_survey_field(farmer, id_farmer=id_farmer)

        if survey_field is None:
            print("\tError no survey field found.")
            rslt = input("Continue - Y, or Break - B\n")
            if rslt == "B":
                break
            else:
                continue

        print("")
        
        ancillary_data = AncillaryData.objects.get(
                survey_field_id=survey_field.id
            )
        row = clean_nan(row)
        populate_ancil_record_as_fall(row, ancillary_data)


def process_height():
    '''For adding height data for
    Fall 2023
    Spring 2023
    Fall 2024
    '''
    fl_height = './data/calcs_from_dan_marzu/23 to 24 weights and heights.xlsx'
    fl_height = './data/23 to 24 weights and heights.xlsx'
    height_data = {
        "2023": {
            "fall": pd.read_excel(fl_height, sheet_name="2023"),
            "spring": pd.read_excel(fl_height, sheet_name="2024 spring")
            },
        "2024": {
            "fall": pd.read_excel(fl_height, sheet_name="2024 fall")
            },
    }
    # height_fall_2023 = pd.read_excel(fl_height, sheet_name="2023")
    # height_spring_2023 = pd.read_excel(fl_height, sheet_name="2024 spring")
    # height_fall_2024 = pd.read_excel(fl_height, sheet_name="2024 fall")
    no_match = {}
    for yr in height_data:
        print(yr)
        for season in height_data[yr]:
            print("\t", season)
            no_match[f"{yr}-{season}"] = []
            
            height_field = "spring_height_of_stand" if season == 'spring' else 'height_of_stand'
            

            for i, row in height_data[yr][season].iterrows():
                
                if yr == "2023":
                    print(f"\t\t{i}: {row['ID']}")
                    if season == "spring":
                        
                        id_col = "description1_spring"
                        # chnage spaces and underscores to hyphens to match data
                        lkup_match = lkup.loc[lkup[id_col].str.replace("_| ", "-") == row['ID']]
                    else:
                        
                        id_col = "description1"
                        lkup_match = lkup.loc[lkup[id_col] == row['ID']]
                        
                    if len(lkup_match) == 0:
                        print("\t\t\tNo match found.")
                        no_match[f"{yr}-{season}"].append(row['ID'])
                        continue
                    lkup_match = lkup_match.to_dict('records')[0]
                    first_name = lkup_match["first_name"]
                    last_name = lkup_match["last_name"]
                    print(f"\t\t\t{first_name} {last_name}")
                    survey_response_id = lkup_match["id"]

                    # John Goodman troubling weirdness
                    if survey_response_id == 49:
                        ancillary_data = AncillaryData.objects.get(survey_field_id=42)
                    else:
                        ancillary_data = AncillaryData.objects.get(
                            survey_response_id=survey_response_id
                        )
                    
                    setattr(ancillary_data, height_field, row['Ave Height'])

                elif yr == "2024":
                    

                    descr = row["ID"]
                    id_farmer = find_farmer(descr)
                    if id_farmer == 85:
                        # JKs second field was given a different ID
                        farmer = Farmer.objects.get(id=55)
                    else:
                        farmer = Farmer.objects.get(id=id_farmer)

                    print(f"Survey for {farmer.first_name} {farmer.last_name}")
                    survey_field = find_survey_field(farmer, id_farmer=id_farmer)
                    try:
                        ancillary_data = AncillaryData.objects.get(
                            survey_field_id=survey_field.id
                        )
                    except AttributeError as e:
                        print("\tNo Ancillary data record.")
                        continue
                    setattr(ancillary_data, height_field, row['Ave Height'])