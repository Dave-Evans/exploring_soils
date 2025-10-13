from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json
from glccp.models import CleanedData


def get_glccp_data(request):

    def get_data_json():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT jsonb_build_object(
                    'type',     'FeatureCollection',
                    'features', jsonb_agg(features.feature)
                )
                FROM (
                  SELECT jsonb_build_object(
                    'type',       'Feature',
                    'id',         id,
                    'geometry',   ST_AsGeoJSON(farm_location)::jsonb,
                    'properties', to_jsonb(inputs) - 'id' - 'farm_location'
                  ) AS feature
                  FROM (
                    SELECT 
                        *
                    FROM (
                        
                            /*cleanup 
                                farm type
                                cover crop type
                                planting method
                                */
                    SELECT id,
                        "year",
                        farm,
                        field, 
                        state,
                        county,
                        zipcode,
                        ag_yrs,
                        case 
                            when farmtype = 'Forage/Row crop' then 'Forage/Row Crop'
                            when trim(farmtype) = 'Row crop' then 'Forage/Row Crop'
                            else trim(farmtype)
                        end as farmtype,
                        soil_texture, 
                        topography, 
                        standing_water, 
                        poor_water_retention, 
                        soilcover, 
                        soilcover_norm, 
                        tillage_intensity_norm_v2, 
                        rotation_div_norm, 
                        orgamend_norm, 
                        cc_history_norm, 
                        cc_div_norm,
                        emi_v2, 
                        case 
                            when cc_current_type = 'Single-species cover crop' then 'Single-species'
                            else cc_current_type
                        end as cc_current_type, 
                        cc_current_overwintering, 
                        cc_current_rate_overwintering, 
                        cc_current_winterkill, 
                        cc_current_rate_winterkill, 
                        fdiversity, 
                        richness, 
                        irrigation, 
                        case
                            when cc_plantstrat = 'Broadcast ,Frost-seeded' then 'Broadcast, Frost-seeded'
                            when cc_plantstrat = 'Broadcast + incorporated' then 'Broadcast + incorporated'
                            when cc_plantstrat = 'Broadcast/incorporated' then 'Broadcast + incorporated'
                            else trim(cc_plantstrat)
                        end as cc_plantstrat,
                        cc_plantdate, 
                        cc_sampledate, 
                        cc_area, 
                        pc, sc, 
                        cc_current_n, 
                        cc_current_n_rate, 
                        cc_current_p,
                        cc_current_p_rate,
                        cc_current_manure, 
                        cc_current_manure_rate, 
                        cc_current_compost, 
                        cc_current_compost_rate, 
                        pc_n, 
                        pc_n_rate, 
                        pc_p, 
                        pc_p_rate, 
                        pc_manure, 
                        pc_manure_rate, 
                        pc_compost,
                        pc_compost_rate,
                        gdd, 
                        precip,
                        weedsuppression, 
                        percent_cover, 
                        agb, 
                        agbn, 
                        farm_location, 
                        image_1, 
                        image_2,
                        image_3
                            from glccp_cleaneddata
                        ) AS geom
                    ) as inputs) features;
            """
            )
            rows = cursor.fetchone()
            data = json.loads(rows[0])
        return data

    data = get_data_json()
    # retrieve signed url for accessing private s3 images
    # There is probably a better way to do this but while there aren't many
    #   submissions this is fine.
    for feat in data["features"]:
        id = feat["id"]

        glccp_record = CleanedData.objects.get(pk=id)
        if glccp_record.image_1:
            feat["properties"]["image_1_url"] = glccp_record.image_1.url
        if glccp_record.image_2:
            feat["properties"]["image_2_url"] = glccp_record.image_2.url
        if glccp_record.image_3:
            feat["properties"]["image_3_url"] = glccp_record.image_3.url

    return JsonResponse(list(data["features"]), safe=False)


def glccp_map(request):
    return render(request, "glccp/map.html")
