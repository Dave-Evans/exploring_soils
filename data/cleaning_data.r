library(dplyr )
library(readxl)
library(ggplot2)
library(lubridate)
library(readr)
library(sf)
library(tidyverse)
library(R.utils)
################################################################################
## For 2022 Data ###############################################################
dat_survey = read_excel("~/Documents/small_projects/wisc_cc/data_from_mrill/CitSci CCROP 2022 responses agronomic.xlsx", sheet = 1)
dat_gdd = read_excel("~/Documents/small_projects/wisc_cc/data_from_mrill/CitSci_GDU_pcp_2022_gs.xlsx", sheet = 1)
dat_biomass = read_excel("~/Documents/small_projects/wisc_cc/data_from_mrill/Table 1. DS draft 2.13.22 CCROP Citizen Science Data 2022 with termination.xlsx",
                         sheet = 1,
                         skip = 1)
dat_forage_q = read_excel("~/Documents/small_projects/wisc_cc/data_from_mrill/Table 1. DS draft 2.13.22 CCROP Citizen Science Data 2022 with termination.xlsx",
                          sheet = 2, range = "A1:I59")
dat_species = read_excel("~/Documents/small_projects/wisc_cc/data_from_mrill/Table 2. for CCROP 2022 (w ID).xlsx",
                         sheet = 1)

dat_survey %>%
  left_join(dat_gdd, by = join_by("ID (zipcode-initials-signup year)" == "id")) %>%
  left_join(dat_biomass, by = join_by("ID (zipcode-initials-signup year)" == `...1`)) %>%
  left_join(dat_forage_q, by = join_by("ID (zipcode-initials-signup year)" == `...1`)) %>%
  left_join(dat_species, by = join_by("ID (zipcode-initials-signup year)" == `ID#`)) %>% 
  
  rename(id = "ID (zipcode-initials-signup year)") %>%
  rename(old_id = "old version of our ID system (zipcode-initials-signup year)") %>%
  rename(county = "1. In what county do you farm? (If you farm in more than one, list them in order of number of acres.)") %>%
  rename(years_experience = "3. How many total years experience do you have planting cover crops?"  ) %>%
  rename(zipcode = "15. Closest zip code for this field (so we can determine appropriate climate data and generate a location map of participating fields). Field must be located in Wisconsin.") %>%
  rename(cc_species_raw = "18. Please select any of the following that were planted as a cover crop in this field this year.") %>%    
  rename(previous_crop = "19. Previous crop in field") %>%
  rename(cash_crop_planting_date = "20. What date this year did you plant your cash crop in this field?") %>%
  rename(dominant_soil_texture = "22. Please choose the dominant soil texture of the field.") %>%
  rename(manure_prior = "23. Will you apply manure prior to seeding cover crops on this field?") %>%
  rename(manure_post = "24. Will manure be applied to the field after the cover crop is established?") %>%
  rename(manure_rate = "25. What manure application rate are you targeting to apply prior to or after establishing your cover crop?") %>%
  rename(manure_value = "25a. Type in number corresponding to selection above in 25.") %>%
  rename(tillage_system = "26. What is your tillage system for the cash crop preceding the cover crop?"  ) %>%
  rename(tillage_equip_primary = "26a.  Primary tillage equipment (select all that apply) for a cash crop preceding a cover crop?") %>%
  rename(tillage_equip_secondary = "26b. Secondary tillage equipment (select all that apply) for cash crop preceding the cover crop?") %>%
  rename(soil_conditions = "27. Soil conditions in this field at cover crop seeding") %>%
  rename(cc_seeding_method = "28. Cover Crop Seeding Method.") %>%
  rename(cc_planting_rate = "29. At what rate did you plant your cover crops (please type species and pounds per acre).") %>%
  rename(cc_termination = "33. Estimated termination timing for this field.") %>%
  rename(days_between_crop_hvst_and_cc_estd = "34. Number of days estimated between crop harvest and cover crop establishment in this field.") %>%
  
  # Growing degree days
  rename(cc_planting_date = "cc_plant") %>%
  rename(days_from_plant_to_bio_hrvst = "dayCount") %>%
  rename(acc_gdd = accGDD) %>%
  rename(total_precip = totalPrecip) %>%
  
  # Forage quality sheet 1
  #rename(cc_species = "multipspecies mix = 5 or more cover crop species planted") %>%
  rename(cc_biomass_collection_date = 'Date collected') %>%
  rename(cc_biomass = "ton DM/ac") %>%
  
  # Forage quality sheet 2
  rename(fq_CP = "CP") %>%
  rename(fq_aNDF = "aNDF") %>%
  rename(fq_uNDFom30 ="uNDFom30") %>%
  rename(fq_NDFD30 = "NDFD30") %>%
  rename(fq_TDN_ADF = "TDN_ADF") %>%
  rename(fq_milkton = "Milk/Ton_Milk2013") %>%
  rename(fq_RFQ = "RFQ") %>%
  
  mutate(year = 2022) %>%
  # Table 2 sheet for species
  rename(cc_rate_and_species = 'lbs/acre, cover crop species') %>%
  # removing all digits for the rates
  mutate(cc_species = gsub('[0-9]+', '', cc_rate_and_species)) %>% 
  # removing remaining decimals and question mark
  mutate(cc_species = gsub('.', '', cc_species, fixed = TRUE)) %>%
  mutate(cc_species = gsub('?', '', cc_species, fixed = TRUE)) %>%
  # Spell check
  mutate(cc_species = gsub('multipsecies', 'multispecies', cc_species)) %>%
  mutate(cc_species = gsub('Raddish', 'radish', cc_species)) %>%
  mutate(cc_species = gsub('ryegrass', 'rye grass', cc_species)) %>%
  mutate(cc_species = gsub("grass red", "grass, red", cc_species)) %>%
  # Removing cases where there's a hyphen separating
  mutate(cc_species = gsub(' -', ',', cc_species)) %>%
  mutate(cc_species = gsub('- ', '', cc_species)) %>%
  # removing semicolons
  mutate(cc_species = gsub(';', ',', cc_species)) %>%
  # changing double spaces to single
  mutate(cc_species = gsub('  ', ' ', cc_species)) %>%
  # remove trailing and leading white space
  mutate(cc_species = trimws(cc_species)) %>%
  
  mutate(cash_crop_planting_date = ifelse(cash_crop_planting_date == 44819, "9/15", cash_crop_planting_date)) %>%
  mutate(cash_crop_planting_date = ifelse(cash_crop_planting_date == 44713, "6/1", cash_crop_planting_date)) %>%
  mutate(cash_crop_planting_date = ifelse(cash_crop_planting_date == 45200, "10/1", cash_crop_planting_date)) %>%
  mutate(cash_crop_planting_date = ifelse(cash_crop_planting_date == 45187, "9/18", cash_crop_planting_date)) %>%
  mutate(cash_crop_planting_date = parse_date_time(paste(cash_crop_planting_date, "2022", sep="/"), "m/d/Y")) %>%
  
  # change n/a to NA
  mutate(tillage_equip_primary = ifelse(tillage_equip_primary == "n/a", NA, tillage_equip_primary)) %>%
  mutate(tillage_equip_secondary = ifelse(tillage_equip_secondary == "n/a", NA, tillage_equip_secondary)) %>%
  select(
    year,
    id, 
    old_id, 
    county, 
    years_experience, 
    zipcode,
    previous_crop, 
    cash_crop_planting_date, 
    dominant_soil_texture,
    manure_prior, 
    manure_post, 
    manure_rate, 
    manure_value,
    tillage_system, 
    tillage_equip_primary, 
    tillage_equip_secondary,
    soil_conditions, 
    cc_seeding_method, 
    cc_planting_rate, 
    cc_termination,
    days_between_crop_hvst_and_cc_estd, 
    site_lat, 
    site_lon, 
    cc_planting_date,
    anpp, 
    cc_biomass_collection_date, 
    total_precip, 
    acc_gdd, 
    days_from_plant_to_bio_hrvst,
    
    cc_biomass,
    fq_CP, 
    fq_aNDF, 
    fq_uNDFom30, 
    fq_NDFD30, 
    fq_TDN_ADF, 
    fq_milkton, 
    fq_RFQ,
    
    cc_rate_and_species,
    cc_species,
    cc_species_raw
    ) -> dat_2022
  
# write_tsv(dat_2022, "~/Documents/small_projects/wisc_cc/wisc_cc_dat_2022.tsv")

################################################################################

###### For 2020 and 2021 data ##################################################

counties = read_sf("~/Documents/exploring_soils/data/county_nrcs_a_wi.gdb/", layer="county_nrcs_a_wi")

zips = read_sf("~/Documents/small_projects/wisc_cc/tl_2020_us_zcta520/tl_2020_us_zcta520.shp")
zips$centroids <- st_transform(zips, 5070) %>%
  st_centroid() %>% 
  #st_transform(., 4269) %>%
  st_transform(., 4326) %>%
  st_geometry()

zip_lu <- zips %>%
  mutate(lon = unlist(map(centroids,1)),
         lat = unlist(map(centroids,2)))  %>%
  as_tibble() %>%
  mutate(ZCTA5CE20 = as.numeric(ZCTA5CE20)) %>%
  select(
    ZCTA5CE20,
    lon,
    lat
  )
  


dat_20_21 = read_excel("~/Documents/small_projects/wisc_cc/data_from_mrill/MI Copy combined CC_citsci_2020-2021-grs.xlsx", sheet = 1)

dat_20_21 %>%
  # Pull out latitude and longitude
  left_join(zip_lu, by = join_by("zip_code" == "ZCTA5CE20")) %>%
  # Perhaps lump red clover and Dutch white clover together as clover
  #   lump radish mixes together?
  #   annual rye grass mix?
  mutate(cc_species_raw = cc_species) %>%      
  mutate(cc_functional_group_mod = case_when(
    cc_species == "annual ryegrass, radish" ~ "annual rye grass, radish",
    cc_species == "annual rye grass, radish" ~ "annual rye grass, radish",
    cc_species == "annual ryegrass" ~ "annual rye grass",
    cc_species == "winter wheat" ~ "wheat (winter)",
    cc_species == "barley, wheat (winter)" ~ "barley, wheat (winter)",
    cc_species == "cereal (winter) rye, oats" ~ "cereal (winter) rye, oats",
    cc_species == "cereal (winter) rye, radish" ~ "cereal (winter) rye, radish",
    cc_species == "cereal (winter) rye" ~ "cereal (winter) rye",
    cc_species == "oats" ~ "oats",
    cc_species == "red clover" ~ "red clover",
    cc_species == "triticale" ~ "triticale",
    cc_species == "radish, red clover" ~ "multispecies mix",
    cc_species == "radish, winter wheat" ~ "multispecies mix",
    cc_functional_group == "multisp_mix" ~ "multispecies mix"
  )) %>%
  # Need to clean up dates in 
  # cc_plant_date, cc_sample_date, est_cc_term_date
  mutate(
    cc_plant_date_mod = case_when(
      !grepl("/", cc_plant_date) ~ as.Date(as.numeric(cc_plant_date), origin = "1899-12-30"),
      .default = as.Date(cc_plant_date, format="%m/%d/%Y"))
  ) %>%
  mutate(
    cc_plant_sample_mod = case_when(
      !grepl("/", cc_sample_date) ~ as.Date(as.numeric(cc_sample_date), origin = "1899-12-30"),
      .default = as.Date(cc_sample_date, format="%m/%d/%Y"))
  ) %>%  
  mutate(
    est_cc_term_date_mod = case_when(
      !grepl("/", est_cc_term_date) ~ as.Date(as.numeric(est_cc_term_date), origin = "1899-12-30"),
      .default = as.Date(est_cc_term_date, format="%m/%d/%Y"))
  ) %>%  
  
  mutate(id = paste(ID, substr(year, 3, 4), sep = '-') ) %>%
  mutate(old_id = paste(ID, substr(year, 3, 4), sep = '-') ) %>%
  mutate(years_experience = cc_experience_y ) %>%
  mutate(zipcode = zip_code ) %>%
  mutate(previous_crop = prev_crop ) %>%
  mutate(cash_crop_planting_date = NA ) %>%
  mutate(dominant_soil_texture = soil_type ) %>%
  mutate(manure_prior = pre_cc_manure ) %>%
  mutate(manure_post = post_cc_manure ) %>%
  mutate(manure_rate = manure_units ) %>%
  mutate(manure_value = manure_rate_target ) %>%
  mutate(tillage_system = mc_tillage_sys ) %>%
  mutate(tillage_equip_primary = mc_tillage_1_equip ) %>%
  mutate(tillage_equip_secondary = mc_tillage_2_equip ) %>%
  mutate(soil_conditions = soil_cond_cc_seeding ) %>%
  # mutate(cc_seeding_method = cc_seeding_method ) %>%
  mutate(cc_planting_rate = cc_seeding_rate_lb_ac ) %>%
  mutate(cc_termination = cc_termination_timing ) %>%
  # What is cc_planting lag? Is this correct?
  mutate(days_between_crop_hvst_and_cc_estd = cc_planting_lag ) %>%
  mutate(site_lat = lat ) %>%
  mutate(site_lon = lon ) %>%
  mutate(cc_planting_date = cc_plant_date_mod ) %>%
  mutate(anpp = '' ) %>%
  mutate(cc_biomass_collection_date = cc_plant_sample_mod ) %>%
  mutate(total_precip = precip_in ) %>%
  # Verify this and isn't GDUcount
  mutate(acc_gdd = GDU_b40 ) %>%
  # Make this cc_planting_date - cc_biomass_collection_date
  mutate(days_from_plant_to_bio_hrvst = '' ) %>%
  # Verify this is correct
  mutate(cc_biomass = Ton_ac ) %>%
  
  mutate(fq_CP = NA ) %>%
  mutate(fq_aNDF = NA ) %>%
  mutate(fq_uNDFom30 = NA ) %>%
  mutate(fq_NDFD30 = NA ) %>%
  mutate(fq_TDN_ADF = NA ) %>%
  mutate(fq_milkton = NA ) %>%
  mutate(fq_RFQ = NA ) %>%
  
  mutate(cc_rate_and_species = cc_species) %>%
  mutate(cc_species = cc_functional_group_mod ) %>%

  select(
    year,
    id, 
    old_id, 
    county, 
    years_experience, 
    zipcode,
    previous_crop, 
    cash_crop_planting_date, 
    dominant_soil_texture,
    manure_prior, 
    manure_post, 
    manure_rate, 
    manure_value,
    tillage_system, 
    tillage_equip_primary, 
    tillage_equip_secondary,
    soil_conditions, 
    cc_seeding_method, 
    cc_planting_rate, 
    cc_termination,
    days_between_crop_hvst_and_cc_estd, 
    site_lat, 
    site_lon, 
    cc_planting_date,
    anpp, 
    cc_biomass_collection_date, 
    total_precip, 
    acc_gdd, 
    days_from_plant_to_bio_hrvst,
    
    cc_biomass,
    fq_CP, 
    fq_aNDF, 
    fq_uNDFom30, 
    fq_NDFD30, 
    fq_TDN_ADF, 
    fq_milkton, 
    fq_RFQ,
    
    cc_rate_and_species,
    cc_species,
    cc_species_raw
  ) -> dat_20_21

dat_all = rbind(dat_2022, dat_20_21)

dat_all <- dat_all %>%
  mutate(
    cc_biomass = as.numeric(ifelse( cc_biomass == ".", NA, cc_biomass)),
    total_precip = as.numeric(ifelse( total_precip == ".", NA, total_precip)),
    acc_gdd = as.numeric(ifelse( acc_gdd == ".", NA, acc_gdd)),
    days_between_crop_hvst_and_cc_estd = as.numeric(ifelse( days_between_crop_hvst_and_cc_estd == ".", NA, days_between_crop_hvst_and_cc_estd)),
    
    dominant_soil_texture = tolower(ifelse( dominant_soil_texture == ".", NA, dominant_soil_texture))
  ) %>%
  mutate(previous_crop = case_when(
    previous_crop == "Rye" ~ "other small grains",
    previous_crop == "Winter Rye" ~ "other small grains",
    previous_crop == "barley" ~ "other small grains",
    previous_crop == "other grain" ~ "other small grains",
    previous_crop == "other grain" ~ "other small grains",
    previous_crop == "corn" ~ "corn for grain",
    previous_crop == "peas" ~ "vegetable crop",
    previous_crop == "green beans" ~ "vegetable crop",
    previous_crop == "Sorghum-sudangrass or forage sorghum" ~"other forage",
    previous_crop == "." ~"other forage",
    .default = previous_crop
  )) %>%
  mutate(
    cc_seeding_method = case_when(
      cc_seeding_method %in% c("drill","drilled","No till drilled") ~ "drill",
      cc_seeding_method == "broadcast, no incorporation" ~ "broadcast",
      cc_seeding_method %in% c("broadcast + incorporation",
                            "broadcast, roll the field",
                            "Broadcast then rolled",
                            "Brillion seeder after wheat",
                            "Billion seeder after wheat;  fall ,cereal rye broadcast+ incorporation",
                            "brillion_bdcst") ~ "broadcast + incorporation",
      cc_seeding_method %in% c("late interseeded -- aerial", "interseeded aerial August 26", "late interseeded -- broadcast") ~ "interseed (late)",
      cc_seeding_method == "early interseeded -- broadcast" ~ "interseed (early)",
      cc_seeding_method == "frost seeded" ~ "frost seed",
      cc_seeding_method == "I don’t remember which field we r talking about." ~ NA,
      cc_seeding_method == "planter_15in" ~ NA,
      .default = cc_seeding_method
    )
  )  %>%
  mutate(residue_remaining = case_when(
    grepl("15-30%", tillage_system) ~ "Reduced, 15-30% residue remaining",
    grepl(">30%", tillage_system) ~ "Conservation, >30% residue remaining",
    grepl("none", tolower(tillage_system)) ~ "Conservation, >30% residue remaining",
    grepl("notill", tolower( gsub("-", "", gsub(" ", "", tillage_system) ) )) ~ "Conservation, >30% residue remaining",
    grepl("<15%", tillage_system) ~ "Conventional, <15% residue remaining",
    grepl("deep ripping", tolower(tillage_system)) ~ "Conventional, <15% residue remaining",
    grepl("organic", tolower(tillage_system)) ~ "Conventional, <15% residue remaining",
    .default = tillage_system
  )) %>% 
  # group_by(tillage_system, residue_remaining) %>%
  # summarise(n= n()) %>%
  # select(tillage_system, residue_remaining, n) -> tst
  
  # select(id, residue_remaining, tillage_system) %>% print(n=100)
  
  mutate(manure_prior = ifelse(manure_prior == ".", "No", manure_prior)) %>%
  mutate(manure_post = ifelse(manure_post == ".", "No", manure_post)) %>%
  mutate(manure_post = ifelse(is.na(manure_post), "No", manure_post)) %>%
  
  mutate(manure_rate = ifelse(manure_rate == ".", NA, manure_rate)) %>%
  mutate(manure_value = ifelse(is.na(manure_value), 0, manure_value)) %>%
  mutate(county_single = ifelse(county == "Trempealeau Buffalo", "Trempealeau", county)) %>%
  mutate(county_single = str_split_i(county_single, ",", 1)) %>% 
  mutate(county_single = str_split_i(county_single, "&", 1)) %>% 
  mutate(county_single = gsub(".", '', county_single, fixed=TRUE)) %>%
  mutate(county_single = capitalize(county_single)) %>%
  mutate(county_single = gsub(" lac", " Lac", county_single)) %>%
  mutate(county_single = gsub(" lake", " Lake", county_single)) %>%
  mutate(county_single = gsub(" croix", " Croix", county_single)) %>%
  mutate(county_single = gsub("St ", "St. ", county_single)) %>% 
  mutate(county_single = trimws(county_single) )
                    
  # select(county_single) %>% unique(.) %>% print(., n=50)
    
    
#     tillage_system = ifelse( tolower(gsub("-", "", gsub(" ", "", tillage_system))) == "notill", "no till", tillage_system),
#     tillage_equip_primary = ifelse( tillage_equip_primary %in% c('n/a', '.', 'nothing', 'None notill'), NA, tillage_equip_primary)
    

write_tsv(dat_all, "~/Documents/small_projects/wisc_cc/wisc_cc_dat.tsv")
dat_all = read_tsv("~/Documents/small_projects/wisc_cc/wisc_cc_dat.tsv")

dat_all %>%
  group_by(cc_species_raw, cc_species) %>%
  summarise(n = n()) -> dat
view(dat)
