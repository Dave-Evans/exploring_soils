import pandas as pd
from pypdf import PdfReader
import os
import re

# Get value from text list dairyland
# Given a value "Moisture" or "Nel 3x Mcal/cwt"
# Return the value or lost

def pull_agsource_2024_fall():
    dir_2024 = "2024/fall/2024 SHC FALL data"
    dirs = os.listdir(dir_2024)
    dirs = [x for x in dirs if os.path.isdir(os.path.join(dir_2024, x))]



def pull_dairyland_2022():

    def find_values(search_string):
        pat = re.compile(search_string)

        for line in splt_text:
            rslt = pat.search(line)
            if rslt is not None:
                print(line)
                cleaned = line.replace(rslt.group(0), '').strip()
                return cleaned

    dir_2022 = "2022"

    dairyland_dir = os.path.join(dir_2022, "dairyland")
    fls_dairyland = os.listdir(dairyland_dir)
    output_2022 = os.path.join(dir_2022, "dairyland_output.csv")

    all_records = []
    list_ids = []
    pat = re.compile("(22)([A-Z]{2})([0-9]{5})")
    for fl in fls_dairyland:
        reader = PdfReader(os.path.join(dairyland_dir, fl))
        #page = reader.pages[0]
        splt_text = []
        for page in reader.pages:
            text = page.extract_text()
            splt_text += text.split("\n")


        for line in splt_text:
            rslt = pat.search(line)
            if rslt:
                cleaned_id = "-".join(rslt.group(3, 2, 1))
                print(f"{cleaned_id}")
                
                break
            else:
                cleaned_id = None

        if cleaned_id in list_ids:
            print(f"Already have {cleaned_id}")
            continue
        if cleaned_id is None:
            continue
        
        list_ids.append(cleaned_id)
        # Sometimes missing a value and there is no blank and cant' automatically determine which is missing
        # negs = splt_text[66].replace("Neg Mcal/cwt ", "").split(" ")
        negs = find_values("Neg Mcal/cwt").split(" ")
        neg_adf_mcal_cwt, neg_oardc_mcal_cwt, neg_milk2013_mcal_cwt = (None, None, None)
        if len(negs) == 3:
            neg_adf_mcal_cwt = negs[0]
            neg_oardc_mcal_cwt = negs[1]
            neg_milk2013_mcal_cwt = negs[2]
        nems = find_values("Nem Mcal/cwt").split(" ")
        nem_adf_mcal_cwt, nem_oardc_mcal_cwt, nem_milk2013_mcal_cwt = (None, None, None)
        if len(nems) == 3:
            nem_adf_mcal_cwt = nems[0]
            nem_oardc_mcal_cwt = nems[1]
            nem_milk2013_mcal_cwt = nems[2]            



        

        record = {
            "field_id": find_values("Product:"),
            "cleaned_id": cleaned_id,
            "sample_date": find_values("Sample Date: "),
            "lab_sample_number": find_values("Sample No.:"),
            "moisture": find_values("Moisture").replace("%", ""),
            "dry_matter": find_values("Dry Matter").replace("%", ""),
            "cp_percdm": find_values("Crude Protein %DM").split(" ")[0],
            "ad_icp_perc_cp": find_values("AD-ICP % of CP %CP").split(" ")[0],
            "nd_icp_perc_cp": find_values("ND-ICP w/SS %CP").split(" ")[0],
            "sol_protein_perc_cp": find_values("Protein Sol. %CP").split(" ")[0],
            "adf_perc_dm": find_values("ADF %DM").split(" ")[0],
            "andf_perc_dm": find_values("aNDF %DM ").split(" ")[0], 
            "andfom_perc_dm": find_values("aNDFom %DM ").split(" ")[0],
            "lignin_perc_ndfom": find_values("Lignin %NDFom ").split(" ")[0],
            "ndfd30_perc_ndfom": find_values("NDFD 30 %NDFom ").split(" ")[0],
            "ndfd240_perc_ndfom": find_values("NDFD240 %NDFom ").split(" ")[0],
            "undfdom30_perc_dm": find_values("uNDFom30 %DM ").split(" ")[0],
            "undfdom240_perc_dm": find_values("uNDFom240 %DM ").split(" ")[0],
            "sugar_esc_perc_dm": find_values("Sugar \(ESC\) %DM ").split(" ")[0],
            "sugar_wsc_perc_dm": find_values("Sugar \(WSC\) %DM ").split(" ")[0],
            "starch_perc_dm": find_values("Starch %DM ").split(" ")[0],
            "fat_ee_perc_dm": find_values("Fat \(EE\) %DM ").split(" ")[0],
            "tfa_fat_perc_dm": find_values("TFA \(fat\) %DM ").split(" ")[0],
            "ash_perc_dm": find_values("Ash %DM ").split(" ")[0],
            "calcium_perc_dm": find_values("Calcium %DM ").split(" ")[0],
            "phosphorus_perc_dm": find_values("Phosphorus %DM ").split(" ")[0],            
            "magnesium_perc_dm": find_values("Magnesium %DM ").split(" ")[0],
            "potassium_perc_dm": find_values("Potassium %DM ").split(" ")[0],
            "sulfur_perc_dm": find_values("Sulfur %DM ").split(" ")[0],
            "chloride_perc_dm": find_values("Chloride %DM ").split(" ")[0],
            "nfc_perc_dm": find_values("NFC %DM").split(" ")[0] if find_values("NFC %DM") else None,
            "nsc_perc_dm": find_values("NSC %DM ").split(" ")[0] if find_values("NSC %DM") else None,
            "rfv_perc_dm": find_values("RFV ").split(" ")[0],            
            "rfq_perc_dm": find_values("RFQ").split(" ")[0] if find_values("RFQ") else None,                        
            "ndf_kid_rate_per_hr": find_values("NDF kd rate MIR_P1 \%/hr ").split(" ")[0],
            "adj_cp_perc_dm": find_values("Adjusted Crude Protein %DM ").split(" ")[0],
            "tdn_adf_perc_dm": find_values("TDN %DM ").split(" ")[0],
            "tdn_oardc_perc_dm": find_values("TDN %DM ").split(" ")[1],
            "tdn_milk2013_perc_dm": find_values("TDN %DM ").split(" ")[2],
            "nel3x_adf_mcal_cwt": find_values("Nel 3x Mcal/cwt ").split(" ")[0],
            "nel3x_oardc_mcal_cwt": find_values("Nel 3x Mcal/cwt ").split(" ")[1],
            "nel3x_milk2013_mcal_cwt": find_values("Nel 3x Mcal/cwt ").split(" ")[2],
            
            "neg_adf_mcal_cwt": neg_adf_mcal_cwt,
            "neg_oardc_mcal_cwt": neg_oardc_mcal_cwt,
            "neg_milk2013_mcal_cwt": neg_milk2013_mcal_cwt,
            
            "nem_adf_mcal_cwt": nem_adf_mcal_cwt,
            "nem_oardc_mcal_cwt": nem_oardc_mcal_cwt,
            "nem_milk2013_mcal_cwt": nem_milk2013_mcal_cwt,
            "milk2013_lbs_per_ton": find_values("Milk per ton lbs/ton ").split(" ")[0],
        }
        all_records.append(record)
    pd.DataFrame(all_records).to_csv(output_2022, index=False)
        

def pull_agsource_2022():

    dir_2022 = "2022"

    agsource_file = os.path.join(dir_2022, "agsource_Dan_Smith_T41498.pdf")
    output_2022 = os.path.join(dir_2022, "agsource_output.csv")

    all_records = []
    reader = PdfReader(agsource_file)
    pat = re.compile("([A-Z]{2})([0-9]{5})")

    #page = reader.pages[0]
    for page in reader.pages:
        text = page.extract_text()
        splt_text = text.split("\n")
        
        cleaned_id = None
        rslt = pat.search(splt_text[14])
        if rslt:
            cleaned_id = "-".join( rslt.group(2, 1) ) + "-22"
            
        record = {


        "field_id": splt_text[14].replace("Field ID: ", ""),
        "cleaned_id": cleaned_id,
        "received_date": splt_text[11][:10],

        "percent_carbon": splt_text[17], #: 46.10
        "percent_nitrogen": splt_text[18], #: 1.26
        "percent_sulfur": splt_text[19], #: 0.16
        "percent_sodium": splt_text[20], #: 0.05
        "percent_calcium": splt_text[21], #: 0.78
        "percent_magnesium": splt_text[22], #: 0.27
        "percent_potassium": splt_text[23], #: 1.15
        "percent_phosphorus": splt_text[24], #: 0.24
        "ppm_boron": splt_text[25], #: 11.7
        "ppm_aluminum": splt_text[26], #: 1978.6
        "ppm_copper": splt_text[27], #: 8.2
        "ppm_manganese": splt_text[28], #: 103.4
        "ppm_zinc": splt_text[29], #: 38.6
        "ppm_iron": splt_text[30], #: 1947.4
        "fresh_wt_g": splt_text[31], #: 471.7
        "dry_matter_perc": splt_text[32], #: 89.56
        "nitrogen_lbs_acre": splt_text[102], #: 127.8
        "phosphorus_lbs_acre": splt_text[103], #: 55.7
        "potassium_lbs_acre": splt_text[104], #: 139.9
        "calcium_lbs_acre": splt_text[105], #: 79.1
        "magnesium_lbs_acre": splt_text[106], #: 27.4
        "sodium_lbs_acre": splt_text[107], #: 4.9
        "sulfur_lbs_acre": splt_text[108], #: 16.2
        "zinc_lbs_acre": splt_text[109], #: 0.39
        "manganese_lbs_acre": splt_text[110], #: 1.05
        "copper_lbs_acre": splt_text[111], #: 0.08
        "iron_lbs_acre": splt_text[112], #: 19.75
        "boron_lbs_acre": splt_text[113], #: 0.12
        "aluminum_lbs_acre": splt_text[114], #: 20.06
        "carbon_lbs_acre": splt_text[115], #: 4674.4
        "c_n_ratio": splt_text[116], #: 36.6
        "fresh_biomass_tons_acre": splt_text[117], #: 5.66
        "dry_biomass_tons_acre": splt_text[118], #: 5.07
        }
        all_records.append(record)
    
    
    df = pd.DataFrame(all_records)
    df.to_csv(output_2022, index=False)

