import pandas as pd


def derive_species_class(survey_response):
    """Takes a wisccc_survey object and classifies
    the given species into a reduced number of classes
    """
    cc_sp_1 = survey_response.cover_crop_species_1
    cc_sp_2 = survey_response.cover_crop_species_2
    cc_sp_3 = survey_response.cover_crop_species_3
    cc_sp_4 = survey_response.cover_crop_species_4
    cc_sp_5 = survey_response.cover_crop_species_5

    # annual rye grass and red clover
    if (cc_sp_1 in ("ANNUAL_RYEGRASS", "RED_CLOVER")) and (
        cc_sp_2 in ("ANNUAL_RYEGRASS", "RED_CLOVER")
    ):
        return "annual rye grass, red clover"

    # annual rye grass and radish
    if (cc_sp_1 in ("ANNUAL_RYEGRASS", "RADISH")) and (
        cc_sp_2 in ("ANNUAL_RYEGRASS", "RADISH")
    ):
        return "annual rye grass, radish"

    # Barley and winter wheat
    if (cc_sp_1 in ("BARLEY", "WHEAT_WINTER")) and (
        cc_sp_2 in ("BARLEY", "WHEAT_WINTER")
    ):
        return "barley, wheat (winter)"

    # cereal rye and hairy vetch
    if (cc_sp_1 in ("CEREAL_RYE", "HAIRY_VETCH")) and (
        cc_sp_2 in ("CEREAL_RYE", "HAIRY_VETCH")
    ):
        return "cereal (winter) rye, hairy vetch"

    # cereal rye and oats
    if (cc_sp_1 in ("CEREAL_RYE", "OATS")) and (cc_sp_2 in ("CEREAL_RYE", "OATS")):
        return "cereal (winter) rye, oats"

    # cereal rye and radish
    if (cc_sp_1 in ("CEREAL_RYE", "RADISH")) and (cc_sp_2 in ("CEREAL_RYE", "RADISH")):
        return "cereal (winter) rye, radish"

    # # oats and peas
    # if (cc_sp_1 in ("OATS", "PEAS")) and (cc_sp_2 in ("OATS", "PEAS")):
    #     return "oats, peas"

    # # oats and radish
    # if (cc_sp_1 in ("OATS", "RADISH")) and (cc_sp_2 in ("OATS", "RADISH")):
    #     return "oats, radish"

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
    if cc_sp_1 == "multispecies mix of 2 or more":
        return "multispecies mix"

    # when only one answer given corresponding to a class
    if (cc_sp_1 == "ANNUAL_RYEGRASS") and not any([cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]):
        return "annual ryegrass"

    if (cc_sp_1 == "CEREAL_RYE") and not any([cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]):
        return "cereal (winter) rye"

    if (cc_sp_1 == "RED_CLOVER") and not any([cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]):
        return "red clover"

    if cc_sp_1 == "OATS":
        return "oats or oat mix"

    if (cc_sp_1 == "TRITICALE") and not any([cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]):
        return "triticale"

    if (cc_sp_1 == "WHEAT_WINTER") and not any([cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]):
        return "wheat (winter)"

    # keep null if all null
    if not all([cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]):
        return None

    if cc_sp_1 in ["OTHER", "OTHER_LEGUME", "OTHER_GRASS"]:
        return "other"

    return "other - escaped"
