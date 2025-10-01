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
                        select 
                            /*cleanup 
                                farm type
                                cover crop type
                                planting method
                                */
                            *
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
