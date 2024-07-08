import json
import pandas as pd

from django.db import connection


def give_species_options(plumbing):
    """Helper function: a lookup for how the cover crop name is formatted.
    2023 and further (collected via django app) will use all caps and abrev (plumbing)
    but 2020-2022 will be formatted as human ready."""
    sp_dct = {
        "ANNUAL_RYEGRASS": "ANNUAL_RYEGRASS" if plumbing else "annual ryegrass",
        "BALANSA_CLOVER": "BALANSA_CLOVER" if plumbing else "balansa clover",
        "BARLEY": "BARLEY" if plumbing else "barley",
        "BERSEEM_CLOVER": "BERSEEM_CLOVER" if plumbing else "berseem clover",
        "BUCKWHEAT": "BUCKWHEAT" if plumbing else "buckwheat",
        "CANOLA": "CANOLA" if plumbing else "canola/rapeseed",
        "CEREAL_RYE": "CEREAL_RYE" if plumbing else "cereal (winter) rye",
        "CRIMSON_CLOVER": "CRIMSON_CLOVER" if plumbing else "crimson clover",
        "COWPEA": "COWPEA" if plumbing else "cowpea",
        "DUTCH_WHITE_CLOVER": (
            "DUTCH_WHITE_CLOVER" if plumbing else "Dutch white clover"
        ),
        "FIELD_PEA": "FIELD_PEA" if plumbing else "field/forage pea",
        "FLAX": "FLAX" if plumbing else "flax",
        "HAIRY_VETCH": "HAIRY_VETCH" if plumbing else "hairy vetch",
        "KALE": "KALE" if plumbing else "kale",
        "MILLET": "MILLET" if plumbing else "millet",
        "PEAS": "PEAS" if plumbing else "peas",
        "PLANTAIN": "PLANTAIN" if plumbing else "plantain",
        "OATS": "OATS" if plumbing else "oats",
        "OTHER_LEGUME": "OTHER_LEGUME" if plumbing else "other (legume)",
        "OTHER_GRASS": "OTHER_GRASS" if plumbing else "other (grass)",
        "OTHER_BROADLEAF": "OTHER_BROADLEAF" if plumbing else "other (broadleaf)",
        "PEARL_MILLET": "PEARL_MILLET" if plumbing else "pearl millet",
        "RADISH": "RADISH" if plumbing else "radish",
        "RED_CLOVER": "RED_CLOVER" if plumbing else "red clover",
        "SORGHUM": "SORGHUM" if plumbing else "sorghum",
        "SORGHUM_SUDAN": "SORGHUM_SUDAN" if plumbing else "sorghum-sudan",
        "SOYBEANS": "SOYBEANS" if plumbing else "soybeans",
        "SUNFLOWER": "SUNFLOWER" if plumbing else "sunflower",
        "SUN_HEMP": "SUN_HEMP" if plumbing else "sun hemp",
        "TRITICALE": "TRITICALE" if plumbing else "triticale",
        "TURNIP": "TURNIP" if plumbing else "turnip",
        "WHEAT_SPRING": "WHEAT_SPRING" if plumbing else "wheat (spring)",
        "WHEAT_WINTER": "WHEAT_WINTER" if plumbing else "wheat (winter)",
        "WINTER_PEA": "WINTER_PEA" if plumbing else "winter pea",
        "YELLOW_SWEET_CLOVER": (
            "YELLOW_SWEET_CLOVER" if plumbing else "yellow sweet clover"
        ),
        "MULITSPECIES": "MULITSPECIES" if plumbing else "multispecies mix of 2 or more",
        "OTHER": "OTHER" if plumbing else "other",
    }

    return sp_dct


def derive_species_class_old(cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5):
    """Takes five wiscc survey species and classifies
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
        return "annual ryegrass mix"

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
        cc_sp_1
        in [
            sp_dct["RED_CLOVER"],
            sp_dct["BERSEEM_CLOVER"],
            sp_dct["CRIMSON_CLOVER"],
            sp_dct["COWPEA"],
            sp_dct["FIELD_PEA"],
            sp_dct["HAIRY_VETCH"],
            sp_dct["OTHER_LEGUME"],
            "Dutch white clover",
        ]
    ) or (
        (
            cc_sp_1
            in [
                sp_dct["RED_CLOVER"],
                sp_dct["BERSEEM_CLOVER"],
                sp_dct["CRIMSON_CLOVER"],
                sp_dct["COWPEA"],
                sp_dct["FIELD_PEA"],
                sp_dct["HAIRY_VETCH"],
                sp_dct["OTHER_LEGUME"],
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
        return "annual ryegrass mix"

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


def derive_species_class_gregg(cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5):
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

    # Winter cereals
    if (cc_sp_1 == sp_dct["ANNUAL_RYEGRASS"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "winter cereal"
    if (cc_sp_1 == sp_dct["CEREAL_RYE"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "winter cereal"
    if (cc_sp_1 == sp_dct["TRITICALE"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "winter cereal"
    if (cc_sp_1 == sp_dct["WHEAT_WINTER"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "winter cereal"
    if (cc_sp_1 == "rye") and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "winter cereal"
    if (cc_sp_1 == "triticale") and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "winter cereal"
    if (cc_sp_1 == "winter wheat") and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "winter cereal"

    # Spring Cereal
    if (cc_sp_1 == sp_dct["BARLEY"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "spring cereal"
    if (cc_sp_1 == sp_dct["OATS"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "spring cereal"
    if cc_sp_1 == "Oats and 3 lb of raddish":
        return "spring cereal"
    if (cc_sp_1 == sp_dct["WHEAT_SPRING"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "spring cereal"

    # Brassica
    if (cc_sp_1 == sp_dct["TURNIP"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "brassica"
    if (cc_sp_1 == sp_dct["RADISH"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "brassica"
    if (cc_sp_1 == sp_dct["CANOLA"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "brassica"
    if (cc_sp_1 == sp_dct["KALE"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "brassica"

    # GRASS
    if (cc_sp_1 == sp_dct["SORGHUM"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "grass"
    if (cc_sp_1 == sp_dct["SORGHUM_SUDAN"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "grass"
    if (cc_sp_1 == sp_dct["OTHER_GRASS"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "grass"

    # Legume Perennial
    if (cc_sp_1 == sp_dct["RED_CLOVER"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "perennial legume"
    if (cc_sp_1 == "Dutch white clover") and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "perennial legume"
    # if (cc_sp_1 == sp_dct["DUTCH_WHITE_CLOVER"]) and not any(
    #     [cc_sp_3, cc_sp_4, cc_sp_5]
    # ):
    #     return "perennial legume"

    # Legume Annual
    if (cc_sp_1 == sp_dct["BERSEEM_CLOVER"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "annual legume"
    if (cc_sp_1 == sp_dct["CRIMSON_CLOVER"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "annual legume"
    if (cc_sp_1 == sp_dct["COWPEA"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "annual legume"
    if (cc_sp_1 == sp_dct["FIELD_PEA"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "annual legume"
    if (cc_sp_1 == sp_dct["HAIRY_VETCH"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "annual legume"
    if (cc_sp_1 == sp_dct["OTHER_LEGUME"]) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "annual legume"

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

    # keep null if all null
    if not any([cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]):
        return None

    if cc_sp_1 in [
        sp_dct["OTHER"],
        sp_dct["OTHER_BROADLEAF"],
    ]:
        return "other"

    # return "other"
    return "other - escaped"


def derive_species_class_gregg_mod(cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5):
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

    # Cereals/Grasses
    # Cereal (winter) rye
    if (cc_sp_1 == sp_dct["CEREAL_RYE"]) and not any(
        [cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]
    ):
        return "Cereal (winter) rye"
    # Winter wheat
    if (cc_sp_1 == sp_dct["WHEAT_WINTER"]) and not any(
        [cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]
    ):
        return "Wheat (winter)"
    # Spring wheat
    if (cc_sp_1 == sp_dct["WHEAT_SPRING"]) and not any(
        [cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]
    ):
        return "Wheat (spring)"
    # Oats
    if (cc_sp_1 == sp_dct["OATS"]) and not any([cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]):
        return "Oats"
    # Triticale
    if (cc_sp_1 == sp_dct["TRITICALE"]) and not any(
        [cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]
    ):
        return "Triticale"

    # rye mix (rye and barley, oats, wheat) –  can all be one color
    if (
        (cc_sp_1 == sp_dct["CEREAL_RYE"])
        and (
            cc_sp_2
            in [
                sp_dct["BARLEY"],
                sp_dct["OATS"],
                sp_dct["WHEAT_WINTER"],
                sp_dct["WHEAT_SPRING"],
                "triticale",
            ]
        )
        and not any([cc_sp_3, cc_sp_4, cc_sp_5])
    ):
        return "Rye mix (rye and barley/oats/wheat)"

    # Annual Rye Grass
    if (cc_sp_1 == sp_dct["ANNUAL_RYEGRASS"]) and not any(
        [cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]
    ):
        return "Annual ryegrass"

    # Other (Sorghum-Sudangrass)

    # Legumes
    # Alfalfa
    # Clover and clover mix (typically a small grain or volunteer grain)
    if (
        cc_sp_1
        in [
            sp_dct["RED_CLOVER"],
            sp_dct["CRIMSON_CLOVER"],
            "Dutch white clover",
            sp_dct["BERSEEM_CLOVER"],
        ]
    ) and (
        cc_sp_2
        in [
            sp_dct["OATS"],
            sp_dct["BARLEY"],
            sp_dct["CEREAL_RYE"],
            sp_dct["WHEAT_WINTER"],
            sp_dct["WHEAT_SPRING"],
        ]
        and not any([cc_sp_3, cc_sp_4, cc_sp_5])
    ):
        return "Clover and clover mix"
    if (
        cc_sp_1
        in [
            sp_dct["OATS"],
            sp_dct["BARLEY"],
            sp_dct["CEREAL_RYE"],
            sp_dct["WHEAT_WINTER"],
            sp_dct["WHEAT_SPRING"],
        ]
    ) and (
        cc_sp_2
        in [
            sp_dct["RED_CLOVER"],
            sp_dct["CRIMSON_CLOVER"],
            "Dutch white clover",
            sp_dct["BERSEEM_CLOVER"],
        ]
        and not any([cc_sp_3, cc_sp_4, cc_sp_5])
    ):
        return "Clover and clover mix"

        # Typically annual: Cow peas, sun hemp soybeans, Berseem clover, Balansa etc)
    if (
        cc_sp_1
        in [
            sp_dct["BERSEEM_CLOVER"],
            sp_dct["COWPEA"],
        ]
    ) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "Legume - typically annual"
        # Typically perennial: Crimson clover, red clover, alfalfa, hairy vetch, field peas etc.
    if (
        cc_sp_1
        in [
            sp_dct["RED_CLOVER"],
            sp_dct["CRIMSON_CLOVER"],
            "Dutch white clover",
            sp_dct["FIELD_PEA"],
            sp_dct["HAIRY_VETCH"],
        ]
    ) and not any([cc_sp_3, cc_sp_4, cc_sp_5]):
        return "Legume - typically perennial"
    # Mix of 2 classes of species
    # Legume & Brassica
    if (
        (
            cc_sp_1
            in [
                sp_dct["RED_CLOVER"],
                sp_dct["CRIMSON_CLOVER"],
                "Dutch white clover",
                sp_dct["FIELD_PEA"],
                sp_dct["HAIRY_VETCH"],
                sp_dct["BERSEEM_CLOVER"],
                sp_dct["COWPEA"],
            ]
        )
        and (
            cc_sp_2
            in [sp_dct["RADISH"], sp_dct["KALE"], sp_dct["CANOLA"], sp_dct["TURNIP"]]
        )
        and not any([cc_sp_3, cc_sp_4, cc_sp_5])
    ):
        return "Legume and Brassica"

    if (
        (
            cc_sp_1
            in [sp_dct["RADISH"], sp_dct["KALE"], sp_dct["CANOLA"], sp_dct["TURNIP"]]
        )
        and (
            cc_sp_2
            in [
                sp_dct["RED_CLOVER"],
                sp_dct["CRIMSON_CLOVER"],
                "Dutch white clover",
                sp_dct["FIELD_PEA"],
                sp_dct["HAIRY_VETCH"],
                sp_dct["BERSEEM_CLOVER"],
                sp_dct["COWPEA"],
            ]
        )
        and not any([cc_sp_3, cc_sp_4, cc_sp_5])
    ):
        return "Legume and Brassica"
    # Small Grain & Brassica
    if (
        (
            cc_sp_1
            in [
                sp_dct["WHEAT_WINTER"],
                sp_dct["WHEAT_SPRING"],
                sp_dct["OATS"],
                sp_dct["BARLEY"],
                sp_dct["CEREAL_RYE"],
            ]
        )
        and (
            cc_sp_2
            in [sp_dct["RADISH"], sp_dct["KALE"], sp_dct["CANOLA"], sp_dct["TURNIP"]]
        )
        and not any([cc_sp_3, cc_sp_4, cc_sp_5])
    ):
        return "Small grain and Brassica"
    if (
        (
            cc_sp_1
            in [sp_dct["RADISH"], sp_dct["KALE"], sp_dct["CANOLA"], sp_dct["TURNIP"]]
        )
        and (
            cc_sp_2
            in [
                sp_dct["WHEAT_WINTER"],
                sp_dct["WHEAT_SPRING"],
                sp_dct["OATS"],
                sp_dct["BARLEY"],
                sp_dct["CEREAL_RYE"],
            ]
        )
        and not any([cc_sp_3, cc_sp_4, cc_sp_5])
    ):
        return "Small grain and Brassica"
    # Legume and small grain
    if (
        (
            cc_sp_1
            in [
                sp_dct["WHEAT_WINTER"],
                sp_dct["WHEAT_SPRING"],
                sp_dct["OATS"],
                sp_dct["BARLEY"],
                sp_dct["CEREAL_RYE"],
            ]
        )
        and (
            cc_sp_2
            in [
                sp_dct["RED_CLOVER"],
                sp_dct["CRIMSON_CLOVER"],
                "Dutch white clover",
                sp_dct["FIELD_PEA"],
                sp_dct["HAIRY_VETCH"],
                sp_dct["BERSEEM_CLOVER"],
                sp_dct["COWPEA"],
            ]
        )
        and not any([cc_sp_3, cc_sp_4, cc_sp_5])
    ):
        return "Small grain and Legume"
    if (
        (
            cc_sp_1
            in [
                sp_dct["RED_CLOVER"],
                sp_dct["CRIMSON_CLOVER"],
                "Dutch white clover",
                sp_dct["FIELD_PEA"],
                sp_dct["HAIRY_VETCH"],
                sp_dct["BERSEEM_CLOVER"],
                sp_dct["COWPEA"],
            ]
        )
        and (
            cc_sp_2
            in [
                sp_dct["WHEAT_WINTER"],
                sp_dct["WHEAT_SPRING"],
                sp_dct["OATS"],
                sp_dct["BARLEY"],
                sp_dct["CEREAL_RYE"],
            ]
        )
        and not any([cc_sp_3, cc_sp_4, cc_sp_5])
    ):
        return "Small grain and Legume"
    # Multispecies mix (≥ 3)

    # Grouping the multispecies
    # When there are five crops listed
    if all([cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]):
        return "Multispecies mix (≥ 3)"

    # When there are four crops listed
    if all([cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4]):
        return "Multispecies mix (≥ 3)"

    # When there are three crops listed
    if all([cc_sp_1, cc_sp_2, cc_sp_3]):
        return "Multispecies mix (≥ 3)"

    # When mulitspecies is selected
    if cc_sp_1 == sp_dct["MULITSPECIES"]:
        return "Multispecies mix (≥ 3)"

    # for past years write in
    if cc_sp_1 == "Terra life maizepro cover crop mix":
        return "Multispecies mix (≥ 3)"

    # keep null if all null
    if not any([cc_sp_1, cc_sp_2, cc_sp_3, cc_sp_4, cc_sp_5]):
        return None

    if cc_sp_1 in [
        sp_dct["OTHER"],
        sp_dct["OTHER_BROADLEAF"],
    ]:
        return "other"

    # return "other"
    return "other - escaped"


def derive_species_class(list_species):
    """Takes a wisccc_survey object and classifies
    the given species into a reduced number of classes
    cereal (winter) rye only
    annual ryegrass only
    legumes
    grasses/cereals
    mix of legumes + grass/cereal + brassica
    mix of legumes + grass/cereal
    mix of grass/cereal + brassica
    other
    """

    # keep null if all null
    if list_species is None or list_species[0] == "." or list_species[0] is None:
        return None

    sp_dct = give_species_options(list_species[0].isupper())

    # for past years write in
    if list_species[0] == sp_dct["MULITSPECIES"]:
        return "mix of legumes + grass/cereal + brassica"

    if list_species[0] == "Terra life maizepro cover crop mix":
        return "mix of legumes + grass/cereal + brassica"

    if list_species[0] in [
        sp_dct["OTHER"],
        sp_dct["OTHER_BROADLEAF"],
    ]:
        return "other"

    # if only annual ryegrass
    # For older years
    if len(list_species) == 1:
        if list_species == [sp_dct["ANNUAL_RYEGRASS"]]:
            return "annual ryegrass only"
    # For 2023+ years
    if len(list_species) == 5:
        # Ensuring that all others are blank
        if list_species[0] == sp_dct["ANNUAL_RYEGRASS"] and list_species[1:] == [
            "",
            "",
            "",
            "",
        ]:
            return "annual ryegrass only"

    # if only cereal rye
    if len(list_species) == 1:
        if list_species == [sp_dct["CEREAL_RYE"]]:
            return "cereal (winter) rye only"

    if len(list_species) == 5:
        if list_species[0] == sp_dct["CEREAL_RYE"] and list_species[1:] == [
            "",
            "",
            "",
            "",
        ]:
            return "cereal (winter) rye only"

    # Family based classese
    list_family = [convert_to_plant_family(sp) for sp in list_species]

    if (
        "brassica" in list_family
        and "grass_cereal" in list_family
        and "legume" in list_family
    ):
        return "mix of legumes + grass/cereal + brassica"

    if "brassica" in list_family and "grass_cereal" in list_family:
        return "mix of grass/cereal + brassica"

    if "brassica" in list_family and "legume" in list_family:
        return "mix of legumes + brassica"

    if "grass_cereal" in list_family and "legume" in list_family:
        return "mix of legumes + grass/cereal"

    if "brassica" in list_family:
        return "radishes, turnips, and other brassicas"

    if "grass_cereal" in list_family:
        return "grasses/cereals"

    if "legume" in list_family:
        return "legumes"

    # return "other"
    return "other - escaped"


def convert_to_plant_family(species):
    """For converting a cc species
    to its plant 'family'

    """
    sp_dct = give_species_options(species.isupper())

    dct_family = {
        # leaving this out for now
        # "broadleaf": ["PHACELIA", "SUNFLOWER"],
        "brassica": ["TURNIP", "RADISH", "KALE", "CANOLA"],
        "legume": [
            "BALANSA_CLOVER",
            "BERSEEM_CLOVER",
            "COWPEA",
            "CRIMSON_CLOVER",
            "DUTCH_WHITE_CLOVER",
            "FIELD_PEA",
            "PEAS",
            "HAIRY_VETCH",
            "OTHER_LEGUME",
            "SOYBEANS",
            "RED_CLOVER",
            "YELLOW_SWEET_CLOVER",
        ],
        "grass_cereal": [
            "ANNUAL_RYEGRASS",
            "BARLEY",
            "BUCKWHEAT",
            "CEREAL_RYE",
            "FLAX",
            "OATS",
            "OTHER_GRASS",
            "PEARL_MILLET",
            "SORGHUM",
            "SORGHUM_SUDAN",
            "SUNFLOWER",
            "TRITICALE",
            "WHEAT_SPRING",
            "WHEAT_WINTER",
            "PLANTAIN",
            "OTHER_BROADLEAF",
        ],
    }

    for family in dct_family:
        for specie_family in dct_family[family]:
            if species == sp_dct[specie_family]:
                print(f"\t{species} is classed as {family}")
                return family

    if species == "dwarf essex rape":
        return "brassica"

    return None


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
        if cc[-3] is None:
            print("Null for", cc[1])
            continue
        id = cc[1]
        # if id in ["53034-RH-22", "54733-AB-20"]:
        #     break
        old_class = cc[-4]

        cc_sps = cc[-3].split(", ")

        species_class = derive_species_class(cc_sps)

        update_static_species(id, species_class)


def update_2023_plus():
    from wisccc.models import Survey

    surveys = Survey.objects.all()
    for survey_response in surveys:

        cc_sp_1 = survey_response.cover_crop_species_1
        cc_sp_2 = survey_response.cover_crop_species_2
        cc_sp_3 = survey_response.cover_crop_species_3
        cc_sp_4 = survey_response.cover_crop_species_4
        cc_sp_5 = survey_response.cover_crop_species_5
        list_sp = [
            survey_response.cover_crop_species_1,
            survey_response.cover_crop_species_2,
            survey_response.cover_crop_species_3,
            survey_response.cover_crop_species_4,
            survey_response.cover_crop_species_5,
        ]

        species_class = derive_species_class(list_sp)
        # if species_class == "other - escaped":
        #     print("_________________")
        #     print("Escaped:")
        #     print(list_sp)
        #     print(survey_response.cover_crop_species_and_rate_write_in)
        #     print(survey_response.cover_crop_multispecies_mix_write_in)
        #     print("_________________")
        # else:
        #     print(species_class)

        survey_response.derived_species_class = species_class
        survey_response.save()


def reclass_all_cc_species():
    # update 2020 - 2022
    update_2020_2022()
    # update 2023+
    update_2023_plus()