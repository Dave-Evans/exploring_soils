from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from wisccc.forms import SurveyForm1, SurveyForm2, SurveyForm3, FarmerForm
from wisccc.models import Survey, Farmer


def wisc_cc_home(request):
    return render(request, "wisccc/wisc_cc_home.html")


# @login_required(login_url="signupFarmer")
def wisc_cc_survey(request):
    template = "wisccc/wisc_cc_survey.html"
    return render(request, template)


def wisc_cc_survey0(request):
    try:
        instance = Farmer.objects.filter(user_id=request.user.id).first()
    except:
        instance = Farmer.objects.create(user_id=request.user.id)

    form = FarmerForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()

        return redirect("wisc_cc_survey")

    # template = "wisccc/survey_upload_all.html"
    template = "wisccc/survey_section_0.html"
    return render(
        request,
        template,
        {
            "form": form,
        },
    )


@login_required
def wisc_cc_survey1(request):
    try:
        instance = Survey.objects.filter(user_id=request.user.id).earliest(
            "last_updated"
        )
    except:
        instance = Survey.objects.create(user_id=request.user.id)

    form = SurveyForm1(request.POST or None, instance=instance)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()

        return redirect("wisc_cc_survey2")

    # template = "wisccc/survey_upload_all.html"
    template = "wisccc/survey_section_1.html"
    return render(
        request,
        template,
        {
            "form": form,
        },
    )


@login_required
def wisc_cc_survey2(request):
    try:
        instance = Survey.objects.filter(user_id=request.user.id).earliest(
            "last_updated"
        )
    except:
        instance = Survey.objects.create(user_id=request.user.id)

    form = SurveyForm2(request.POST or None, instance=instance)

    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()

        return redirect("wisc_cc_survey3")

    template = "wisccc/survey_section_2.html"
    return render(
        request,
        template,
        {
            "form": form,
        },
    )


@login_required
def wisc_cc_survey3(request):
    try:
        instance = Survey.objects.filter(user_id=request.user.id).earliest(
            "last_updated"
        )
    except:
        instance = Survey.objects.create(user_id=request.user.id)

    form = SurveyForm3(request.POST or None, instance=instance)

    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()

        return redirect("wisc_cc_survey3")

    template = "wisccc/survey_section_3.html"
    return render(
        request,
        template,
        {
            "form": form,
        },
    )


def wisc_cc_graph(request):
    return render(request, "wisccc/wisc_cc_graph.html")


def wisc_cc_map(request):
    return render(request, "wisccc/wisc_cc_map_toggle.html")


def wisc_cc_map_v2(request):
    return render(request, "wisccc/wisc_cc_map_toggle.html")


@xframe_options_exempt
def wisc_cc_map_embed(request):
    return render(request, "wisccc/wisc_cc_map_embed.html")


def get_wi_counties(request):
    # from django.db import connection

    def get_county_json():
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
                    'geometry',   ST_AsGeoJSON(geom)::jsonb,
                    'properties', to_jsonb(inputs) - 'geom' - 'id'
                  ) AS feature
                  FROM (
                    SELECT 
                            objectid as id 
                            , countyname
                            , shape as geom
                            from wi_counties
                    ) as inputs
                ) features;
            """
            )
            rows = cursor.fetchone()
            data = json.loads(rows[0])
        return data

    data = get_county_json()

    return JsonResponse(data, safe=False)


# For accessing data from previous years survey
def wisc_cc_static_data(request):
    def get_json():
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
                    'geometry',   ST_AsGeoJSON(collectionpoint)::jsonb,
                    'properties', to_jsonb(inputs) - 'id' - 'collectionpoint'
                  ) AS feature
                  FROM (
                    SELECT 
                            geom.id
                            , geom.year
                            , geom.county
                            , geom.county_single
                            , geom.years_experience
                            , geom.zipcode
                            , geom.previous_crop
                            , geom.cash_crop_planting_date 
                            , geom.dominant_soil_texture
                            , geom.manure_prior 
                            , geom.manure_post
                            , geom.manure_rate 
                            , geom.manure_value 
                            , geom.tillage_system 
                            , geom.tillage_equip_primary
                            , geom.tillage_equip_secondary
                            , geom.residue_remaining
                            , geom.soil_conditions
                            , geom.cc_seeding_method
                            , geom.cc_planting_rate
                            , geom.cc_termination
                            , geom.days_between_crop_hvst_and_cc_estd
                            , geom.cc_planting_date
                            , geom.anpp
                            , geom.cc_biomass_collection_date
                            , geom.total_precip
                            , geom.acc_gdd
                            , geom.days_from_plant_to_bio_hrvst
                            , geom.cc_biomass
                            , geom.fq_cp
                            , geom.fq_andf
                            , geom.fq_undfom30
                            , geom.fq_ndfd30
                            , geom.fq_tdn_adf
                            , geom.fq_milkton
                            , geom.fq_rfq
                            , geom.cc_rate_and_species
                            , geom.cc_species
                            , ST_GeometryN(ST_GeneratePoints(geom.b_collectionpoint, 1), 1) as collectionpoint 
                        FROM (
                            select 
                                *, ST_Buffer(ST_SetSRID(ST_MakePoint(site_lon, site_lat), 4326), 0.02) as b_collectionpoint
                                from wisc_cc wc
                            ) AS geom
                    ) as inputs) features;
            """
            )
            rows = cursor.fetchone()
            data = json.loads(rows[0])
        return data

    data = get_json()

    return JsonResponse(list(data["features"]), safe=False)
