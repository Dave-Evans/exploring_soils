from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import connection
import json
import djqscsv
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django_tables2 import RequestConfig
from wisccc.tables import (
    ResponseTable,
)
from wisccc.forms import (
    SurveyForm1,
    SurveyForm2,
    SurveyForm3,
    FarmerForm,
    FullSurveyForm,
)
from wisccc.models import Survey, Farmer
from wisccc.data_mgmt import pull_all_years_together, get_survey_data
import pandas as pd


# REVISE WITH NEW STRUCTURE
#   This will be dependent on how the forms shake out.
def check_section_completed(user_id, section):
    """Checks a particular section, farmer, 1, 2, 3
    to see if a particualr required field is a completed."""

    if section == "farmer":
        farmer = Farmer.objects.filter(user_id=user_id).first()
        if farmer is None:
            return False
        if farmer.last_name == "" or farmer.last_name is None:
            return False

        return True

    if section == 1:
        survey = Survey.objects.filter(user_id=user_id).first()
        if survey is None:
            return False
        if survey.percent_of_farm_cc is None:
            return False

        return True

    if section == 2:
        survey = Survey.objects.filter(user_id=user_id).first()
        if survey is None:
            return False
        if survey.closest_zip_code is None:
            return False

        return True

    if section == 3:
        survey = Survey.objects.filter(user_id=user_id).first()
        if survey is None:
            return False
        if survey.additional_thoughts is None:
            return False

        return True


def wisc_cc_home(request):
    return render(request, "wisccc/wisc_cc_home.html")


@permission_required("wisccc.survery_manager", raise_exception=True)
def wisccc_download_data(request):
    # qs = Survey.objects.raw(query)
    # return djqscsv.render_to_csv_response(qs)
    df = get_survey_data()
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = "attachment; filename=survey_data.csv"

    df.to_csv(path_or_buf=resp, sep=",", index=False)
    return resp


@login_required
def wisc_cc_survey(request):
    """Home page for Cover Crop survey. We check progress of different sections of the survey
    by querying one required question from each section (0 (the farmer section),1,2,3).
    If this is completed then we assume it is all completed."""

    completed_0 = check_section_completed(request.user.id, "farmer")
    completed_1 = check_section_completed(request.user.id, 1)
    completed_2 = check_section_completed(request.user.id, 2)
    completed_3 = check_section_completed(request.user.id, 3)

    template = "wisccc/wisc_cc_survey.html"

    return render(
        request,
        template,
        {
            "completed_0": completed_0,
            "completed_1": completed_1,
            "completed_2": completed_2,
            "completed_3": completed_3,
        },
    )


# REVISE each survey page according to each form
@login_required
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
            "farmer_form": form,
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
        # Here classify species
        new_form.derive_species_class()
        new_form.populate_county()
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

        return redirect("wisc_cc_survey")

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


def get_wisc_cc_data(request):
    data = pull_all_years_together("json")

    return JsonResponse(list(data["features"]), safe=False)


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
                            , geom.cc_species_raw
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


# class SurveyResponseDeleteView(PermissionRequiredMixin, DeleteView):
#     permission_required = "wisccc.survery_manager"
#     model = Survey
#     success_url = reverse_lazy("kanopy_table")


# class SurveyResponseUpdateView(PermissionRequiredMixin, UpdateView):
#     permission_required = "wisccc.survery_manager"
#     model = Survey
#     form_class = FullSurveyForm
#     template_name = "wisccc/update_form.html"
#     success_url = reverse_lazy("kanopy_table")


@permission_required("wisccc.survery_manager", raise_exception=True)
def response_table(request):
    """List wisc response entries"""
    all_surveys = Survey.objects.all()
    total_surveys = all_surveys.count()
    completed_surveys = (
        all_surveys.filter(percent_of_farm_cc__isnull=False)
        .filter(closest_zip_code__isnull=False)
        .filter(additional_thoughts__isnull=False)
        .count()
    )

    # REVISE!
    #   Revise according to new structure
    def get_table_data():
        """For getting survey data and returning an excel doc"""
        query = """
            select 
                s.id as id
                , u.username 
                , u.email
                , f.first_name 
                , f.last_name
                , s.survey_created::Date
                , s.confirmed_accurate
            from wisccc_survey s 
            left join wisccc_farmer f
            on s.user_id = f.user_id 
            left join auth_user as u
            on s.user_id = u.id"""
        dat = pd.read_sql(query, connection)
        dat = dat.to_dict("records")

        return dat

    data = get_table_data()

    # table = ResponseTable(Survey.objects.all())
    table = ResponseTable(data)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    return render(
        request,
        "wisccc/response_table.html",
        {
            "table": table,
            "total_surveys": total_surveys,
            "completed_surveys": completed_surveys,
        },
    )


@permission_required("wisccc.survery_manager", raise_exception=True)
def delete_response(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Survey, id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("response_table")

    return render(request, "wisccc/delete_response.html", context)


@permission_required("wisccc.survery_manager", raise_exception=True)
def update_response(request, id):
    """For updating survey"""
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Survey, id=id)

    farmer = Farmer.objects.filter(user_id=obj.user_id).first()

    # pass the object as instance in form
    form = FullSurveyForm(request.POST or None, instance=obj)

    farmer_form = FarmerForm(request.POST or None, instance=farmer)
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid() and farmer_form.is_valid():
        form.save()
        # Here verify county
        # Here calc gdu?
        farmer_form.save()
        return redirect("response_table")
    # add form dictionary to context
    context["form"] = form
    context["farmer_form"] = farmer_form

    return render(request, "wisccc/survey_review.html", context)
