import pandas as pd
from django.contrib.auth.models import User
from wisccc.models import AncillaryData, SurveyFarm, SurveyField

# Spring 2023 (2024)
fl_dairyland_spring_23 = (
    "./data/labdata_2023/spring_lab_data/SHC 2023-2024 Dairyland Labs data.csv"
)
fl_nutrient_spring_23 = "./data/labdata_2023/spring_lab_data/BN5905 UW COVER_CROP.CSV"

# Fall 2023
fl_dairyland_fall_23 = (
    "./data/labdata_2023/dairyland_labs_forage_analysis_data_2023.csv"
)
fl_nutrient_fall_23 = "./data/labdata_2023/bn05905_p_cover_crop2023_biomass.csv"
# Cross walk between lab IDs and old survey_response_ids
fl_lkup = "./data/labdata_2023/all_lab_data_2023.tsv"

# Key is column in AncillaryData,
#   Value is column header
# Dairyland: Dry_Matter, uNDFom240, RFV



dct_cols = {
    
    # "uNDFom240": "uNDFom240",
    # "dry_matter": "Dry_Matter",    
    # "rfv": "RFV",
    "c_to_n_ratio" : "C-N Ratio",
    "total_nitrogen" : "Total Nitrogen",
    "percent_p" : "P",
    "percent_k" : "K",
    "percent_ca" : "Ca",        
    "percent_mg" : "Mg",
    "percent_s" : "S",
    # "n_content" : "nitrogen_lbs_acre",
    "p_content" : "P2O5 Lbs/Acre",
    "k_content" : "K2O Lbs/Acre",
    "ca_content" : "Ca Lbs/Acre",     
    "mg_content" : "Mg Lbs/Acre",     
    "s_content" : "S Lbs/Acre",
    "c_content" : "Carbon Lbs/Acre"
}



def populate_2023_spring_and_fall():
    # dairyland_fall23 = pd.read_csv(fl_dairyland_fall_23)
    # dairyland_spring23 = pd.read_csv(fl_dairyland_spring_23)

    agsource_fall23 = pd.read_csv(fl_nutrient_fall_23)
    agsource_spring23 = pd.read_csv(fl_nutrient_spring_23)

    dct_seasons = {
        "spring": agsource_spring23,
        "fall": agsource_fall23,
    }

    lkup = pd.read_csv(fl_lkup, sep="\t")
    for i, row in lkup.iterrows():

        first_name = row["first_name"]
        last_name = row["last_name"]
        survey_response_id = row["id"]

        if survey_response_id in [57, 41, 59]:
            continue

        # John Goodman troubling weirdness
        if survey_response_id == 49:
            ancillary_data = AncillaryData.objects.get(survey_field_id=42)
        else:
            ancillary_data = AncillaryData.objects.get(
                survey_response_id=survey_response_id
            )

        farmer = ancillary_data.survey_field.survey_farm.farmer
        db_first_name = farmer.first_name
        db_last_name = farmer.last_name

        print(f"Lookup: {first_name} {last_name}")
        print(f"DB: {db_first_name} {db_last_name}")

        # fall = dairyland_fall.loc[
        #     dairyland_fall["Description1"] == row["description1"],
        #     ["Dry_Matter", "RFV", "uNDFom240"],
        # ].to_dict("records")
        # spring = dairyland_spring.loc[
        #     dairyland_spring["Description 1"] == row["grower_name"],
        #     ["Dry Matter", "RFV", "uNDFom240"],
        # ].to_dict("records")
        # fall = agsource_fall23.loc[
        #     agsource_fall23["Grower Name"] == row["grower_name"],
        # ].to_dict("records")
        for season in dct_seasons:
            print(season)
            if season == "spring":
                id_col = "grower_name_spring"
            else:
                id_col = "grower_name"
            record = dct_seasons[season].loc[
                dct_seasons[season]["Grower Name"] == row[id_col],
            ].to_dict("records")

            
            if len(record) > 1:
                print("\t-------------")
                print("\tMore than one record returned from lab sheet!")
                print("\t-------------")
                break
            
            if len(record) == 0:
                print("\t-------------")
                print("\tNo record found.")
                print("\t-------------")
                continue

            record = record[0]

            
            for key in dct_cols:
                val = dct_cols[key]
                if season == "spring":
                    field_name = "spring_" + key
                else:
                    field_name = key
                
                setattr(ancillary_data, field_name, record[val])
                ancillary_data.save()

