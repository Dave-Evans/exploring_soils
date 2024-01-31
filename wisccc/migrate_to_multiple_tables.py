from wisccc.models import Survey, SurveyField

surveys = Survey.objects.all()
for srvy in surveys:
    SurveyField.objects.create(
        survey=srvy,
        # Location
        farm_location=srvy.farm_location,
        # In the following section we ask you about your specific cover cropping practices in one field or set of fields (can be one acre ro 1,000) from which you'll take your samples for biomass, nutrient, and forage analysis. Provide answers *for that field.*
        # 16 Closest zip code for this field (so we can determine appropriate climate data and generate a location map of participating fields). Field must be located in Wisconsin.
        closest_zip_code=srvy.closest_zip_code,
        # 17 What is this field(s) acreage?
        field_acreage=srvy.field_acreage,
        crop_rotation=srvy.crop_rotation,
        crop_rotation_2021_cover_crop_species=srvy.crop_rotation_2021_cover_crop_species,
        crop_rotation_2021_cash_crop_species=srvy.crop_rotation_2021_cash_crop_species,
        # 18b.
        crop_rotation_2022_cover_crop_species=srvy.crop_rotation_2022_cover_crop_species,
        crop_rotation_2022_cash_crop_species=srvy.crop_rotation_2022_cash_crop_species,
        # 18c.
        crop_rotation_2023_cover_crop_species=srvy.crop_rotation_2023_cover_crop_species,
        crop_rotation_2023_cash_crop_species=srvy.crop_rotation_2023_cash_crop_species,
        cover_crop_species_1=srvy.cover_crop_species_1,
        cover_crop_planting_rate_1=srvy.cover_crop_planting_rate_1,
        cover_crop_planting_rate_1_units=srvy.cover_crop_planting_rate_1_units,
        # Species 2
        cover_crop_species_2=srvy.cover_crop_species_2,
        cover_crop_planting_rate_2=srvy.cover_crop_planting_rate_2,
        cover_crop_planting_rate_2_units=srvy.cover_crop_planting_rate_2_units,
        cover_crop_species_3=srvy.cover_crop_species_3,
        cover_crop_planting_rate_3=srvy.cover_crop_planting_rate_3,
        cover_crop_planting_rate_3_units=srvy.cover_crop_planting_rate_3_units,
        cover_crop_species_4=srvy.cover_crop_species_4,
        cover_crop_planting_rate_4=srvy.cover_crop_planting_rate_4,
        cover_crop_planting_rate_4_units=srvy.cover_crop_planting_rate_4_units,
        cover_crop_species_5=srvy.cover_crop_species_5,
        cover_crop_planting_rate_5=srvy.cover_crop_planting_rate_5,
        cover_crop_planting_rate_5_units=srvy.cover_crop_planting_rate_5_units,
        cover_crop_species_and_rate_write_in=srvy.cover_crop_species_and_rate_write_in,
        cover_crop_multispecies_mix_write_in=srvy.cover_crop_multispecies_mix_write_in,
        cash_crop_planting_date=srvy.cash_crop_planting_date,
        years_with_cover_crops=srvy.years_with_cover_crops,
        dominant_soil_texture=srvy.dominant_soil_texture,
        manure_prior=srvy.manure_prior,
        manure_prior_rate=srvy.manure_prior_rate,
        manure_prior_rate_units=srvy.manure_prior_rate_units,
        manure_post=srvy.manure_post,
        manure_post_rate=srvy.manure_post_rate,
        manure_post_rate_units=srvy.manure_post_rate_units,
        tillage_system_cash_crop=srvy.tillage_system_cash_crop,
        primary_tillage_equipment=srvy.primary_tillage_equipment,
        primary_tillage_equipment_write_in=srvy.primary_tillage_equipment_write_in,
        secondary_tillage_equipment=srvy.secondary_tillage_equipment,
        secondary_tillage_equipment_write_in=srvy.secondary_tillage_equipment_write_in,
        soil_conditions_at_cover_crop_seeding=srvy.soil_conditions_at_cover_crop_seeding,
        cover_crop_seeding_method=srvy.cover_crop_seeding_method,
        cover_crop_seeding_method_write_in=srvy.cover_crop_seeding_method_write_in,
        cover_crop_seed_cost=srvy.cover_crop_seed_cost,
        cover_crop_planting_cost=srvy.cover_crop_planting_cost,
        cover_crop_planting_date=srvy.cover_crop_planting_date,
        cover_crop_estimated_termination=srvy.cover_crop_estimated_termination,
        days_between_crop_hvst_and_cc_estd=srvy.days_between_crop_hvst_and_cc_estd,
    )
