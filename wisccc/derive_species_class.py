import json
import pandas as pd

from django.db import connection


def give_species_options(plumbing):
    # plumbing = False
    sp_dct = {
        "ANNUAL_RYEGRASS": "ANNUAL_RYEGRASS" if plumbing else "annual ryegrass",
        "BARLEY": "BARLEY" if plumbing else "barley",
        "BERSEEM_CLOVER": "BERSEEM_CLOVER" if plumbing else "berseem clover",
        "CANOLA": "CANOLA" if plumbing else "canola/rapeseed",
        "CEREAL_RYE": "CEREAL_RYE" if plumbing else "cereal (winter) rye",
        "CRIMSON_CLOVER": "CRIMSON_CLOVER" if plumbing else "crimson clover",
        "COWPEA": "COWPEA" if plumbing else "cowpea",
        "FIELD_PEA": "FIELD_PEA" if plumbing else "field/forage pea",
        "HAIRY_VETCH": "HAIRY_VETCH" if plumbing else "hairy vetch",
        "KALE": "KALE" if plumbing else "kale",
        "OATS": "OATS" if plumbing else "oats",
        "OTHER_LEGUME": "OTHER_LEGUME" if plumbing else "other (legume)",
        "OTHER_GRASS": "OTHER_GRASS" if plumbing else "other (grass)",
        "OTHER_BROADLEAF": "OTHER_BROADLEAF" if plumbing else "other (broadleaf)",
        "RADISH": "RADISH" if plumbing else "radish",
        "RED_CLOVER": "RED_CLOVER" if plumbing else "red clover",
        "SORGHUM": "SORGHUM" if plumbing else "sorghum",
        "SORGHUM_SUDAN": "SORGHUM_SUDAN" if plumbing else "sorghum-sudan",
        "SUNFLOWER": "SUNFLOWER" if plumbing else "sunflower",
        "TRITICALE": "TRITICALE" if plumbing else "tritcale",
        "TURNIP": "TURNIP" if plumbing else "turnip",
        "WHEAT_SPRING": "WHEAT_SPRING" if plumbing else "wheat (spring)",
        "WHEAT_WINTER": "WHEAT_WINTER" if plumbing else "wheat (winter)",
        "MULITSPECIES": "MULITSPECIES" if plumbing else "multispecies mix of 2 or more",
        "OTHER": "OTHER" if plumbing else "other",
    }

    return sp_dct


def derive_species_class(cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5):
    """Takes a wisccc_survey object and classifies
    the given species into a reduced number of classes
    """
    # cc_sp_1 = survey_response.cover_crop_species_1
    # cc_sp_2 = survey_response.cover_crop_species_2
    # cc_sp_3 = survey_response.cover_crop_species_3
    # cc_sp_4 = survey_response.cover_crop_species_4
    # cc_sp_5 = survey_response.cover_crop_species_5
    # keep null if all null
    if cc_sp_1 is None or cc_sp_1 == ".":
        return None

    sp_dct = give_species_options(cc_sp_1.isupper())

    # annual rye grass and mix
    # when ryegrass is first and there is up to one other species given.
    if (cc_sp_1 == sp_dct["ANNUAL_RYEGRASS"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "annual ryegrass or annual ryegrass mix"

    # # Barley and winter wheat
    # added the "or" option for write-in of past year
    if cc_sp_1 == sp_dct["BARLEY"]:
        return "barley or barley mix"

    # cereal rye and one other
    if (
        (cc_sp_1 == sp_dct["CEREAL_RYE"])
        and cc_sp_2 is not None
        and not any([cc_sp_3, cc_sp_4, cc_sp_5])
    ):
        return "cereal (winter) rye mix"

    # cereal rye and oats
    # if (cc_sp_1 in (sp_dct["CEREAL_RYE"], sp_dct["OATS"])) and (
    #     cc_sp_2 in (sp_dct["CEREAL_RYE"], sp_dct["OATS"])
    # ):
    #     return "cereal (winter) rye, oats"

    # cereal rye and radish
    # if (cc_sp_1 in (sp_dct["CEREAL_RYE"], sp_dct["RADISH"])) and (
    #     cc_sp_2 in (sp_dct["CEREAL_RYE"], sp_dct["RADISH"])
    # ):
    #     return "cereal (winter) rye, radish"

    # # oats and peas
    # if (cc_sp_1 in ("OATS", "PEAS")) and (cc_sp_2 in ("OATS", "PEAS")):
    #     return "oats, peas"

    # # oats and radish
    # if (cc_sp_1 in ("OATS", "RADISH")) and (cc_sp_2 in ("OATS", "RADISH")):
    #     return "oats, radish"

    # For legume/legume  mix
    if (
        (
            cc_sp_1
            in [
                sp_dct["RED_CLOVER"],
                sp_dct["BERSEEM_CLOVER"],
                sp_dct["CRIMSON_CLOVER"],
                sp_dct["COWPEA"],
                sp_dct["FIELD_PEA"],
                sp_dct["HAIRY_VETCH"],
                "Dutch white clover",
            ]
        )
        or (
            cc_sp_1
            in [
                sp_dct["RED_CLOVER"],
                sp_dct["BERSEEM_CLOVER"],
                sp_dct["CRIMSON_CLOVER"],
                sp_dct["COWPEA"],
                sp_dct["FIELD_PEA"],
                sp_dct["HAIRY_VETCH"],
            ]
        )
        and any([cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5])
    ):
        return "legume or legume mix"

    # added the "or" option for write-in of past year
    if cc_sp_1 == sp_dct["OATS"] or cc_sp_1 == "Oats and 3 lb of raddish":
        return "oats or oat mix"

    # Grouping the multispecies

    # When there are five crops listed
    if all([cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]):
        return "multispecies mix"

    # When there are four crops listed
    if all([cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4]):
        return "multispecies mix"

    # When there are three crops listed
    if all([cc_sp_1, cc_sp_2, cc_sp_3]):
        return "multispecies mix"

    # When mulitspecies is selected
    if cc_sp_1 == sp_dct["MULITSPECIES"]:
        return "multispecies mix"

    # for past years write in
    if cc_sp_1 == "Terra life maizepro cover crop mix":
        return "multispecies mix"

    # when only one answer given corresponding to a class
    if (cc_sp_1 == sp_dct["ANNUAL_RYEGRASS"]) and not any(
        [cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]
    ):
        return "annual ryegrass"

    # Only cereal rye
    if (cc_sp_1 == sp_dct["CEREAL_RYE"]) and not any(
        [cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]
    ):
        return "cereal (winter) rye"

    if (cc_sp_1 == sp_dct["CEREAL_RYE"]) and cc_sp_2 == "triticale":
        return "cereal (winter) rye"

    if cc_sp_1 == "rye":
        return "cereal (winter) rye"

    if (cc_sp_1 == sp_dct["TRITICALE"]) and not any(
        [cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]
    ):
        return "triticale"

    if (cc_sp_1 == sp_dct["WHEAT_WINTER"] or cc_sp_1 == "winter wheat") and not any(
        [cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]
    ):
        return "wheat (winter)"

    if (
        cc_sp_1 in [sp_dct["WHEAT_WINTER"], sp_dct["RADISH"]]
        and cc_sp_2 in [sp_dct["WHEAT_WINTER"], sp_dct["RADISH"], "winter wheat"]
    ) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "wheat (winter)"

    # keep null if all null
    if not any([cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]):
        return None

    if cc_sp_1 in [
        sp_dct["OTHER"],
        sp_dct["OTHER_LEGUME"],
        sp_dct["OTHER_GRASS"],
        sp_dct["OTHER_BROADLEAF"],
    ]:
        return "other"

    return "other"
    # return "other - escaped"


def update_static_species(id, species):
    from django.db import connection

    with connection.cursor() as cursor:
        if species:
            cursor.execute(
                f"""
                    update wisc_cc 
                    set cc_species = '{species}'
                    where id = '{id}'
                    """
            )
        else:
            cursor.execute(
                f"""
                    update wisc_cc 
                    set cc_species = NULL
                    where id = '{id}'
                    """
            )


def update_2020_2022():
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("select * from wisc_cc")
        wisc_cc = cursor.fetchall()

    for i, cc in enumerate(wisc_cc):
        # split the third from last item, raw species
        # unpack first five to variables
        id = cc[1]
        old_class = cc[-4]
        cc_sps = cc[-3].split(", ")[:5]
        # We need five cc species,
        #   this is to pad the list with Nones
        cc_sps = cc_sps + (5 - len(cc_sps)) * [None]
        cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5 = cc_sps

        species = derive_species_class(cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5)
        update_static_species(id, species)


def update_2023_plus():
    from wisccc.models import Survey

    surveys = Survey.objects.all()
    for survey_response in surveys:
        print(survey_response.cover_crop_species_1)
        if survey_response.cover_crop_species_1 == "OTHER_GRASS":
            print("Got one")
            break
        cc_sp_1 = survey_response.cover_crop_species_1
        cc_sp_2 = survey_response.cover_crop_species_2
        cc_sp_3 = survey_response.cover_crop_species_3
        cc_sp_4 = survey_response.cover_crop_species_4
        cc_sp_5 = survey_response.cover_crop_species_5
        survey_response.derived_species_class = derive_species_class(
            survey_response.cover_crop_species_1,
            survey_response.cover_crop_species_2,
            survey_response.cover_crop_species_3,
            survey_response.cover_crop_species_4,
            survey_response.cover_crop_species_5,
        )
        survey_response.save()


def reclass_all_cc_species():
    # update 2020 - 2022
    update_2020_2022()
    # update 2023+
    update_2023_plus()


def pull_all_years_together(f_output):
    """f_output is format of the output:
    sql: for returning just the query
    json: for returning json
    df: for pandas dataframe"""

    query = """
    SELECT 
        stat.id
        , stat.year
        , stat.county
        , stat.county_single
        , stat.years_experience
        , stat.zipcode
        , stat.previous_crop
        , stat.cash_crop_planting_date 
        , stat.dominant_soil_texture
        , stat.manure_prior 
        , null as manure_prior_rate
        , null as manure_prior_rate_units
        , stat.manure_post
        , null manure_post_rate
        , null as manure_post_rate_units
        , stat.manure_rate 
        , stat.manure_value 
        , stat.tillage_system 
        , stat.tillage_equip_primary
        , stat.tillage_equip_secondary
        , stat.residue_remaining
        , stat.soil_conditions
        , stat.cc_seeding_method
        , stat.cc_planting_rate
        , stat.cc_termination
        , stat.days_between_crop_hvst_and_cc_estd
        , stat.site_lon
        , stat.site_lat        
        , stat.cc_planting_date
        
        , stat.anpp
        , stat.cc_biomass_collection_date
        , stat.total_precip
        , stat.acc_gdd
        , stat.days_from_plant_to_bio_hrvst

        , stat.cc_biomass
        , stat.fq_cp
        , stat.fq_andf
        , stat.fq_undfom30
        , stat.fq_ndfd30
        , stat.fq_tdn_adf
        , stat.fq_milkton
        , stat.fq_rfq
        
        , stat.cc_rate_and_species
        , stat.cc_species
        , stat.cc_species_raw
    from wisc_cc as stat

    union all

    select
        wisc_cc_id as id,
        year,
        a.county,
        null as county_single,
        years_experience::text as years_experience,
        closest_zip_code as zipcode,
        mod_crop_rotation_2023_cash_crop_species as previous_crop,
        cash_crop_planting_date,
        lower(replace(dominant_soil_texture, '_', ' ')) as dominant_soil_texture,
        -- Make this yes no? Or change static to boolean?
        case
            when manure_prior = true then 'Yes'
            when manure_prior = false then 'No'
            when manure_prior is null then 'No'
        end as manure_prior,
        manure_prior_rate,
        mod_manure_prior_rate_units as manure_prior_rate_units,
        case
            when manure_post = true then 'Yes'
            when manure_post = false then 'No'
            when manure_post is null then 'No'
        end as manure_post,
        manure_post_rate,
        mod_manure_post_rate_units as mod_manure_post_rate_units,	
        null as manure_rate, 
        null as manure_value, 	
        mod_tillage_system_cash_crop as tillage_system,
        primary_tillage_equipment as tillage_equip_primary,
        secondary_tillage_equipment as tillage_equip_secondary,
        mod_residue_remaining as residue_remaining,	
        lower(soil_conditions_at_cover_crop_seeding) as soil_conditions,
        mod_cc_seeding_method as cc_seeding_method,
        concat(		
            concat(  cover_crop_planting_rate_1, ' ', mod_cover_crop_planting_rate_1_units, ' ', mod_cover_crop_species_1),
            nullif(concat(  ', ', cover_crop_planting_rate_2, ' ', mod_cover_crop_planting_rate_2_units, ' ', mod_cover_crop_species_2), ',   '),
            nullif(concat(  ', ', cover_crop_planting_rate_3, ' ', mod_cover_crop_planting_rate_3_units, ' ', mod_cover_crop_species_3), ',   '),
            nullif(concat(  ', ', cover_crop_planting_rate_4, ' ', mod_cover_crop_planting_rate_4_units, ' ', mod_cover_crop_species_4), ',   '),
            nullif(concat(  ', ', cover_crop_planting_rate_5, ' ', mod_cover_crop_planting_rate_5_units, ' ', mod_cover_crop_species_5), ',   ')
        ) as cc_planting_rate,
        mod_cover_crop_estimated_termination as cc_termination,
        null as days_between_crop_hvst_and_cc_estd,
	    ST_X(farm_location) as site_lon,
	    ST_Y(farm_location) as site_lat,                
        cover_crop_planting_date as cc_planting_date,
        
        null as anpp,
        null as cc_biomass_collection_date,
        null as total_precip,
        null as acc_gdd,
        null as days_from_plant_to_bio_hrvst,

        null as cc_biomass,
        null as fq_cp,
        null as fq_andf,
        null as fq_undfom30,
        null as fq_ndfd30,
        null as fq_tdn_adf,
        null as fq_milkton,
        null as fq_rfq,
        
        concat(		
            concat(  cover_crop_planting_rate_1, ' ', mod_cover_crop_planting_rate_1_units, ' ', mod_cover_crop_species_1),
            nullif(concat(  ', ', cover_crop_planting_rate_2, ' ', mod_cover_crop_planting_rate_2_units, ' ', mod_cover_crop_species_2), ',   '),
            nullif(concat(  ', ', cover_crop_planting_rate_3, ' ', mod_cover_crop_planting_rate_3_units, ' ', mod_cover_crop_species_3), ',   '),
            nullif(concat(  ', ', cover_crop_planting_rate_4, ' ', mod_cover_crop_planting_rate_4_units, ' ', mod_cover_crop_species_4), ',   '),
            nullif(concat(  ', ', cover_crop_planting_rate_5, ' ', mod_cover_crop_planting_rate_5_units, ' ', mod_cover_crop_species_5), ',   ')
        ) as cc_rate_and_species,
        derived_species_class as cc_species,		
        concat(
            mod_cover_crop_species_1, 
            nullif(concat(', ', mod_cover_crop_species_2), ', '), 
            nullif(concat(', ', mod_cover_crop_species_3), ', '), 
            nullif(concat(', ', mod_cover_crop_species_4), ', '), 
            nullif(concat(', ', mod_cover_crop_species_5), ', ')
        ) as cc_species_raw
    from (
        select
            *,
            concat(
                live_dat.closest_zip_code,
                '-',
                upper(substring(wf.first_name, 1, 1)),
                upper(substring(wf.last_name,  1, 1))
            ) as wisc_cc_id,
            date_part('year', live_dat.cover_crop_planting_date) as year,
            case
                when live_dat.cover_crop_species_1 = 'ANNUAL_RYEGRASS' then 'annual ryegrass'
                when live_dat.cover_crop_species_1 = 'BARLEY' then 'barley'
                when live_dat.cover_crop_species_1 = 'BERSEEM_CLOVER' then 'berseem clover'
                when live_dat.cover_crop_species_1 = 'CANOLA' then 'canola/rapeseed'
                when live_dat.cover_crop_species_1 = 'CEREAL_RYE' then 'cereal (winter) rye'
                when live_dat.cover_crop_species_1 = 'CRIMSON_CLOVER' then 'crimson clover'
                when live_dat.cover_crop_species_1 = 'COWPEA' then 'cowpea'
                when live_dat.cover_crop_species_1 = 'FIELD_PEA' then 'field/forage pea'
                when live_dat.cover_crop_species_1 = 'HAIRY_VETCH' then 'hairy vetch'
                when live_dat.cover_crop_species_1 = 'KALE' then 'kale'
                when live_dat.cover_crop_species_1 = 'OATS' then 'oats'
                when live_dat.cover_crop_species_1 = 'OTHER_LEGUME' then 'other (legume)'
                when live_dat.cover_crop_species_1 = 'OTHER_GRASS' then 'other (grass)'
                when live_dat.cover_crop_species_1 = 'OTHER_BROADLEAF' then 'other (broadleaf)'
                when live_dat.cover_crop_species_1 = 'RADISH' then 'radish'
                when live_dat.cover_crop_species_1 = 'RED_CLOVER' then 'red clover'
                when live_dat.cover_crop_species_1 = 'SORGHUM' then 'sorghum'
                when live_dat.cover_crop_species_1 = 'SORGHUM_SUDAN' then 'sorghum-sudan'
                when live_dat.cover_crop_species_1 = 'SUNFLOWER' then 'sunflower'
                when live_dat.cover_crop_species_1 = 'TRITICALE' then 'Tritcale'
                when live_dat.cover_crop_species_1 = 'TURNIP' then 'turnip'
                when live_dat.cover_crop_species_1 = 'WHEAT_SPRING' then 'wheat (spring)'
                when live_dat.cover_crop_species_1 = 'WHEAT_WINTER' then 'wheat (winter)'
                when live_dat.cover_crop_species_1 = 'MULITSPECIES' then 'multispecies mix of 2 or more'
                when live_dat.cover_crop_species_1 = 'OTHER' then 'other'		
            end as mod_cover_crop_species_1,
            case
                when live_dat.cover_crop_species_2 = 'ANNUAL_RYEGRASS' then 'annual ryegrass'
                when live_dat.cover_crop_species_2 = 'BARLEY' then 'barley'
                when live_dat.cover_crop_species_2 = 'BERSEEM_CLOVER' then 'berseem clover'
                when live_dat.cover_crop_species_2 = 'CANOLA' then 'canola/rapeseed'
                when live_dat.cover_crop_species_2 = 'CEREAL_RYE' then 'cereal (winter) rye'
                when live_dat.cover_crop_species_2 = 'CRIMSON_CLOVER' then 'crimson clover'
                when live_dat.cover_crop_species_2 = 'COWPEA' then 'cowpea'
                when live_dat.cover_crop_species_2 = 'FIELD_PEA' then 'field/forage pea'
                when live_dat.cover_crop_species_2 = 'HAIRY_VETCH' then 'hairy vetch'
                when live_dat.cover_crop_species_2 = 'KALE' then 'kale'
                when live_dat.cover_crop_species_2 = 'OATS' then 'oats'
                when live_dat.cover_crop_species_2 = 'OTHER_LEGUME' then 'other (legume)'
                when live_dat.cover_crop_species_2 = 'OTHER_GRASS' then 'other (grass)'
                when live_dat.cover_crop_species_2 = 'OTHER_BROADLEAF' then 'other (broadleaf)'
                when live_dat.cover_crop_species_2 = 'RADISH' then 'radish'
                when live_dat.cover_crop_species_2 = 'RED_CLOVER' then 'red clover'
                when live_dat.cover_crop_species_2 = 'SORGHUM' then 'sorghum'
                when live_dat.cover_crop_species_2 = 'SORGHUM_SUDAN' then 'sorghum-sudan'
                when live_dat.cover_crop_species_2 = 'SUNFLOWER' then 'sunflower'
                when live_dat.cover_crop_species_2 = 'TRITICALE' then 'Tritcale'
                when live_dat.cover_crop_species_2 = 'TURNIP' then 'turnip'
                when live_dat.cover_crop_species_2 = 'WHEAT_SPRING' then 'wheat (spring)'
                when live_dat.cover_crop_species_2 = 'WHEAT_WINTER' then 'wheat (winter)'
                when live_dat.cover_crop_species_2 = 'MULITSPECIES' then 'multispecies mix of 2 or more'
                when live_dat.cover_crop_species_2 = 'OTHER' then 'other'		
            end as mod_cover_crop_species_2,
            case
                when live_dat.cover_crop_species_3 = 'ANNUAL_RYEGRASS' then 'annual ryegrass'
                when live_dat.cover_crop_species_3 =  'BARLEY' then 'barley'
                when live_dat.cover_crop_species_3 = 'BERSEEM_CLOVER' then 'berseem clover'
                when live_dat.cover_crop_species_3 = 'CANOLA' then 'canola/rapeseed'
                when live_dat.cover_crop_species_3 = 'CEREAL_RYE' then 'cereal (winter) rye'
                when live_dat.cover_crop_species_3 = 'CRIMSON_CLOVER' then 'crimson clover'
                when live_dat.cover_crop_species_3 = 'COWPEA' then 'cowpea'
                when live_dat.cover_crop_species_3 = 'FIELD_PEA' then 'field/forage pea'
                when live_dat.cover_crop_species_3 = 'HAIRY_VETCH' then 'hairy vetch'
                when live_dat.cover_crop_species_3 = 'KALE' then 'kale'
                when live_dat.cover_crop_species_3 = 'OATS' then 'oats'
                when live_dat.cover_crop_species_3 = 'OTHER_LEGUME' then 'other (legume)'
                when live_dat.cover_crop_species_3 = 'OTHER_GRASS' then 'other (grass)'
                when live_dat.cover_crop_species_3 = 'OTHER_BROADLEAF' then 'other (broadleaf)'
                when live_dat.cover_crop_species_3 = 'RADISH' then 'radish'
                when live_dat.cover_crop_species_3 = 'RED_CLOVER' then 'red clover'
                when live_dat.cover_crop_species_3 = 'SORGHUM' then 'sorghum'
                when live_dat.cover_crop_species_3 = 'SORGHUM_SUDAN' then 'sorghum-sudan'
                when live_dat.cover_crop_species_3 = 'SUNFLOWER' then 'sunflower'
                when live_dat.cover_crop_species_3 = 'TRITICALE' then 'Tritcale'
                when live_dat.cover_crop_species_3 = 'TURNIP' then 'turnip'
                when live_dat.cover_crop_species_3 = 'WHEAT_SPRING' then 'wheat (spring)'
                when live_dat.cover_crop_species_3 = 'WHEAT_WINTER' then 'wheat (winter)'
                when live_dat.cover_crop_species_3 = 'MULITSPECIES' then 'multispecies mix of 2 or more'
                when live_dat.cover_crop_species_3 = 'OTHER' then 'other'		
            end as mod_cover_crop_species_3,
            case
                when live_dat.cover_crop_species_4 = 'ANNUAL_RYEGRASS' then 'annual ryegrass'
                when live_dat.cover_crop_species_4 = 'BARLEY' then 'barley'
                when live_dat.cover_crop_species_4 = 'BERSEEM_CLOVER' then 'berseem clover'
                when live_dat.cover_crop_species_4 = 'CANOLA' then 'canola/rapeseed'
                when live_dat.cover_crop_species_4 = 'CEREAL_RYE' then 'cereal (winter) rye'
                when live_dat.cover_crop_species_4 = 'CRIMSON_CLOVER' then 'crimson clover'
                when live_dat.cover_crop_species_4 = 'COWPEA' then 'cowpea'
                when live_dat.cover_crop_species_4 = 'FIELD_PEA' then 'field/forage pea'
                when live_dat.cover_crop_species_4 = 'HAIRY_VETCH' then 'hairy vetch'
                when live_dat.cover_crop_species_4 = 'KALE' then 'kale'
                when live_dat.cover_crop_species_4 = 'OATS' then 'oats'
                when live_dat.cover_crop_species_4 = 'OTHER_LEGUME' then 'other (legume)'
                when live_dat.cover_crop_species_4 = 'OTHER_GRASS' then 'other (grass)'
                when live_dat.cover_crop_species_4 = 'OTHER_BROADLEAF' then 'other (broadleaf)'
                when live_dat.cover_crop_species_4 = 'RADISH' then 'radish'
                when live_dat.cover_crop_species_4 = 'RED_CLOVER' then 'red clover'
                when live_dat.cover_crop_species_4 = 'SORGHUM' then 'sorghum'
                when live_dat.cover_crop_species_4 = 'SORGHUM_SUDAN' then 'sorghum-sudan'
                when live_dat.cover_crop_species_4 = 'SUNFLOWER' then 'sunflower'
                when live_dat.cover_crop_species_4 = 'TRITICALE' then 'Tritcale'
                when live_dat.cover_crop_species_4 = 'TURNIP' then 'turnip'
                when live_dat.cover_crop_species_4 = 'WHEAT_SPRING' then 'wheat (spring)'
                when live_dat.cover_crop_species_4 = 'WHEAT_WINTER' then 'wheat (winter)'
                when live_dat.cover_crop_species_4 = 'MULITSPECIES' then 'multispecies mix of 2 or more'
                when live_dat.cover_crop_species_4 = 'OTHER' then 'other'		
            end as mod_cover_crop_species_4,
            case
                when live_dat.cover_crop_species_5 = 'ANNUAL_RYEGRASS' then 'annual ryegrass'
                when live_dat.cover_crop_species_5 = 'BARLEY' then 'barley'
                when live_dat.cover_crop_species_5 = 'BERSEEM_CLOVER' then 'berseem clover'
                when live_dat.cover_crop_species_5 = 'CANOLA' then 'canola/rapeseed'
                when live_dat.cover_crop_species_5 = 'CEREAL_RYE' then 'cereal (winter) rye'
                when live_dat.cover_crop_species_5 = 'CRIMSON_CLOVER' then 'crimson clover'
                when live_dat.cover_crop_species_5 = 'COWPEA' then 'cowpea'
                when live_dat.cover_crop_species_5 = 'FIELD_PEA' then 'field/forage pea'
                when live_dat.cover_crop_species_5 = 'HAIRY_VETCH' then 'hairy vetch'
                when live_dat.cover_crop_species_5 = 'KALE' then 'kale'
                when live_dat.cover_crop_species_5 = 'OATS' then 'oats'
                when live_dat.cover_crop_species_5 = 'OTHER_LEGUME' then 'other (legume)'
                when live_dat.cover_crop_species_5 = 'OTHER_GRASS' then 'other (grass)'
                when live_dat.cover_crop_species_5 = 'OTHER_BROADLEAF' then 'other (broadleaf)'
                when live_dat.cover_crop_species_5 = 'RADISH' then 'radish'
                when live_dat.cover_crop_species_5 = 'RED_CLOVER' then 'red clover'
                when live_dat.cover_crop_species_5 = 'SORGHUM' then 'sorghum'
                when live_dat.cover_crop_species_5 = 'SORGHUM_SUDAN' then 'sorghum-sudan'
                when live_dat.cover_crop_species_5 = 'SUNFLOWER' then 'sunflower'
                when live_dat.cover_crop_species_5 = 'TRITICALE' then 'Tritcale'
                when live_dat.cover_crop_species_5 = 'TURNIP' then 'turnip'
                when live_dat.cover_crop_species_5 = 'WHEAT_SPRING' then 'wheat (spring)'
                when live_dat.cover_crop_species_5 = 'WHEAT_WINTER' then 'wheat (winter)'
                when live_dat.cover_crop_species_5 = 'MULITSPECIES' then 'multispecies mix of 2 or more'
                when live_dat.cover_crop_species_5 = 'OTHER' then 'other'		
            end as mod_cover_crop_species_5,
            case
                when live_dat.cover_crop_planting_rate_1_units = 'POUNDS_ACRE' then 'lbs/acre' 
                when live_dat.cover_crop_planting_rate_1_units = 'BUSHELS_ACRE' then 'bu/acre' 
            end as mod_cover_crop_planting_rate_1_units,	
            case
                when live_dat.cover_crop_planting_rate_2_units = 'POUNDS_ACRE' then 'lbs/acre' 
                when live_dat.cover_crop_planting_rate_2_units = 'BUSHELS_ACRE' then 'bu/acre' 
            end as mod_cover_crop_planting_rate_2_units,	
            case
                when live_dat.cover_crop_planting_rate_3_units = 'POUNDS_ACRE' then 'lbs/acre' 
                when live_dat.cover_crop_planting_rate_3_units = 'BUSHELS_ACRE' then 'bu/acre' 
            end as mod_cover_crop_planting_rate_3_units,	
            case
                when live_dat.cover_crop_planting_rate_4_units = 'POUNDS_ACRE' then 'lbs/acre' 
                when live_dat.cover_crop_planting_rate_4_units = 'BUSHELS_ACRE' then 'bu/acre' 
            end as mod_cover_crop_planting_rate_4_units,	
            case
                when live_dat.cover_crop_planting_rate_5_units = 'POUNDS_ACRE' then 'lbs/acre' 
                when live_dat.cover_crop_planting_rate_5_units = 'BUSHELS_ACRE' then 'bu/acre' 
            end as mod_cover_crop_planting_rate_5_units
            , case	        
                when live_dat.tillage_system_cash_crop  = 'CONVENTIONAL' then 'conventional tillage (<15% residue)'
                when live_dat.tillage_system_cash_crop = 'REDUCED' then 'reduced tillage (15-30% residue)'
                when live_dat.tillage_system_cash_crop = 'MULCH_TILL' then 
                    'conservation tillage (>30% residue) - mulch till/vertical tillage'
                when live_dat.tillage_system_cash_crop = 'STRIP_TILL' then 'conservation tillage (>30% residue) - strip till'
                when live_dat.tillage_system_cash_crop = 'NO_TILL' then 'conservation tillage (>30% residue) - no till'    
            end as mod_tillage_system_cash_crop
            , case	        
                when live_dat.tillage_system_cash_crop = 'CONVENTIONAL' then 'Conventional, <15% residue remaining'
                when live_dat.tillage_system_cash_crop = 'REDUCED' then 'Reduced, 15-30% residue remaining'
                when live_dat.tillage_system_cash_crop = 'MULCH_TILL' then 
                    'Conservation, >30% residue remaining'
                when live_dat.tillage_system_cash_crop = 'STRIP_TILL' then 'Conservation, >30% residue remaining'
                when live_dat.tillage_system_cash_crop = 'NO_TILL' then 'No till'    
            end as mod_residue_remaining
            , case 
                when live_dat.cover_crop_seeding_method = 'FROST' then'frost seeded'
                when live_dat.cover_crop_seeding_method = 'DRILLED' then 'drilled'
                when live_dat.cover_crop_seeding_method = 'BROADCAST_NO_INCORP' then 'broadcast, no incorporation'
                when live_dat.cover_crop_seeding_method = 'EARLY_INTERSEED' then 'early interseeded -- broadcast'
                when live_dat.cover_crop_seeding_method = 'LATE_INTERSEED_BROADCAST' then 'late interseeded -- broadcast'
                when live_dat.cover_crop_seeding_method = 'LATE_INTERSEED_AERIAL' then 'late interseeded -- aerial'
                when live_dat.cover_crop_seeding_method = 'BROADCAST_INCORPORATION' then 'broadcast + incorporation'
                when live_dat.cover_crop_seeding_method = 'FERT_BROADCAST_INCORP' then 'cover crop seed mixed with fertilizer + broadcast + incorporation'
                when live_dat.cover_crop_seeding_method = 'OTHER' then 'other'
            end as mod_cc_seeding_method
            , case 
                when live_dat.manure_prior_rate_units = 'GALLONS' then 'gal/acre'
                when live_dat.manure_prior_rate_units = 'POUNDS_ACRE' then 'lbs/acre'
            end as mod_manure_prior_rate_units
            , case 
                when live_dat.manure_post_rate_units = 'GALLONS' then 'gal/acre'
                when live_dat.manure_post_rate_units = 'POUNDS_ACRE' then 'lbs/acre'
            end as mod_manure_post_rate_units
            , case 
                when live_dat.cover_crop_estimated_termination = 'GRAZE_FALL' then 'graze fall'
                when live_dat.cover_crop_estimated_termination = 'WINTERKILL' then 'little to no cover crop growth in spring'
                when live_dat.cover_crop_estimated_termination = 'FALLKILL' then 'killing frost (fall)'
                when live_dat.cover_crop_estimated_termination = 'GRAZE_SPRING' then 'graze spring'
                when live_dat.cover_crop_estimated_termination = 'SPRING_HERBICIDE' then 'early spring, herbicide application (14 plus days prior to crop establishment)'
                
                when live_dat.cover_crop_estimated_termination = 'FORAGE' then 'harvest for forage'
                when live_dat.cover_crop_estimated_termination = 'GREEN_HERBICIDE' then 'plant green, herbicide termination'
                when live_dat.cover_crop_estimated_termination = 'SPRING_ROLLER_CRIMPER' then 'early spring, roller-crimper termination'
                when live_dat.cover_crop_estimated_termination = 'GREEN_ROLLER_CRIMPER' then 'plant green, roller-crimper termination'
                when live_dat.cover_crop_estimated_termination = 'OTHER' then 'other'
            end as mod_cover_crop_estimated_termination,
            case 
                when live_dat.crop_rotation_2023_cash_crop_species = 'CORN_FOR_GRAIN' then 'corn for grain'
                when live_dat.crop_rotation_2023_cash_crop_species = 'CORN_SILAGE' then 'corn silage'
                when live_dat.crop_rotation_2023_cash_crop_species = 'SOYBEANS' then 'soybeans'
                when live_dat.crop_rotation_2023_cash_crop_species = 'WHEAT' then 'wheat'
                when live_dat.crop_rotation_2023_cash_crop_species = 'OATS' then 'oats'
                when live_dat.crop_rotation_2023_cash_crop_species = 'BARLEY' then 'barley'
                when live_dat.crop_rotation_2023_cash_crop_species = 'TRITICALE' then 'Tritcale'
                when live_dat.crop_rotation_2023_cash_crop_species = 'SORGHUM' then 'sorghum'
                when live_dat.crop_rotation_2023_cash_crop_species = 'SORGHUM_SUDAN' then 'sorghum-sudan'
                when live_dat.crop_rotation_2023_cash_crop_species = 'ALFALFA' then 'alfalfa'
                when live_dat.crop_rotation_2023_cash_crop_species = 'VEGETABLE_CROP' then 'vegetable crop'
                when live_dat.crop_rotation_2023_cash_crop_species = 'OTHER_GRAIN' then 'other grain'
                when live_dat.crop_rotation_2023_cash_crop_species = 'OTHER_FORAGE' then 'other forage'
                when live_dat.crop_rotation_2023_cash_crop_species = 'LIVESTOCK' then 'livestock feeding/grazing'	    	
            end as mod_crop_rotation_2023_cash_crop_species
            
            
            from wisccc_survey as live_dat
            left join wisccc_farmer wf 
            on live_dat.user_id = wf.user_id 
            where live_dat.confirmed_accurate = TRUE

    ) as a
    """

    if f_output == "sql":
        return query

    if f_output == "json":
        query_json = """
            SELECT jsonb_build_object(
                'type',     'FeatureCollection',
                'features', jsonb_agg(features.feature)
            )
            FROM (
            SELECT jsonb_build_object(
                'type',       'Feature',
                'id',         id,
                'geometry',   ST_AsGeoJSON(farmlocation)::jsonb,
                'properties', to_jsonb(inputs) - 'id' - 'farmlocation'
            ) AS feature
            FROM (
                select 
                    *, ST_GeometryN(ST_GeneratePoints(geom.b_farmlocation, 1), 1) as farmlocation 
                from (
                    select
                        *, ST_Buffer(ST_SetSRID(ST_MakePoint(site_lon, site_lat), 4326), 0.02) as b_farmlocation
                    from (
                        {query}
                        ) as b
                    ) as geom
                ) as inputs
            ) features;""".format(
            query=query
        )

        with connection.cursor() as cursor:
            cursor.execute(query_json)
            rows = cursor.fetchone()
            data = json.loads(rows[0])

        return data

    if f_output == "df":
        data = pd.read_sql(query, connection)
        # df.value_counts(['cc_species', 'cc_species_raw'])
        return data