import json
import djqscsv
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import connection
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from wisccc.forms import UserLoginForm
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
from wisccc.tables import ResponseTable, RegistrationTable
from wisccc.forms import (
    SurveyFieldFormFull,
    SurveyFarmFormPart1,
    SurveyFarmFormPart2,
    SurveyFarmFormPart3,
    FieldFarmFormFull,
    SurveyForm1,
    SurveyForm2,
    SurveyForm3,
    FarmerForm,
    FullSurveyForm,
    SurveyFarmFormFull,
    SurveyPhotoForm,
    CustomUserCreationForm,
    SurveyRegistrationFullForm,
    SurveyRegistrationPartialForm,
    UserInfoForm,
)

from wisccc.models import (
    Survey,
    Farmer,
    SurveyPhoto,
    SurveyRegistration,
    SurveyField,
    SurveyFarm,
    FieldFarm,
)
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
def wisc_cc_manager_home(request):
    return render(request, "wisccc/wisc_cc_manager_home.html")


def wisc_cc_about(request):
    return render(request, "wisccc/wisc_cc_about.html")


@permission_required("wisccc.survery_manager", raise_exception=True)
def wisccc_download_data(request, opt):
    # opt == 1 then full survey with qualitative
    # opt == 2 then display data
    if opt == 1:
        df = get_survey_data()
        filename = "full_survey_questions.csv"
    elif opt == 2:
        df = pull_all_years_together("df")
        filename = "cleaned_data_from_display.csv"
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = f"attachment; filename={filename}"

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
    # field names as keys
    context = {}
    survey_year = 2024
    # Don't forget to grab based on survey_year!!!
    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    survey_farm = (
        SurveyFarm.objects.filter(farmer_id=farmer.id)
        .filter(survey_year=survey_year)
        .first()
    )

    # survey_field = get_object_or_404(SurveyField, survey_farm_id=survey_farm.id)
    # field_farm = get_object_or_404(FieldFarm, id=survey_field.field_farm_id)

    # pass the object as instance in form
    survey_farm_form = SurveyFarmFormPart1(request.POST or None, instance=survey_farm)

    # farmer_form = FarmerForm(request.POST or None, instance=farmer)

    # user_info_form = UserInfoForm(request.POST or None, instance=user)

    # form = SurveyForm1(request.POST or None, instance=instance)
    if survey_farm_form.is_valid():
        new_form = survey_farm_form.save(commit=False)
        new_form.farmer = farmer
        # Make sure to make a slot for this in the form.
        # new_form.survey_year = 2024
        new_form.save()

        return redirect("wisc_cc_survey2")

    # template = "wisccc/survey_upload_all.html"
    template = "wisccc/survey_section_1.html"
    return render(
        request,
        template,
        {
            "form": survey_farm_form,
        },
    )


@login_required
def wisc_cc_survey2(request):
    # field names as keys
    context = {}

    # Don't forget to grab based on survey_year!!!
    survey_year = 2024
    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    survey_farm = (
        SurveyFarm.objects.filter(farmer_id=farmer.id)
        .filter(survey_year=survey_year)
        .first()
    )
    if survey_farm is None:
        survey_field = None
    else:
        survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()

    if survey_field is None:
        field_farm = None
    else:
        field_farm = FieldFarm.objects.filter(id=survey_field.field_farm_id).first()

    # pass the object as instance in form
    survey_farm_form = SurveyFarmFormPart2(request.POST or None, instance=survey_farm)

    survey_field_form = SurveyFieldFormFull(request.POST or None, instance=survey_field)

    field_farm_form = FieldFarmFormFull(request.POST or None, instance=field_farm)

    if (
        survey_farm_form.is_valid()
        and survey_field_form.is_valid()
        and field_farm_form.is_valid()
    ):
        # Just save survey_farm because no after the fact additions necessary
        new_survey_farm_form = survey_farm_form.save()

        new_field_farm_form = field_farm_form.save(commit=False)
        new_field_farm_form.farmer = farmer

        new_survey_field_form = survey_field_form.save(commit=False)
        new_survey_field_form.survey_farm = new_survey_farm_form
        new_survey_field_form.field_farm = new_field_farm_form
        # Make sure to save field_farm first
        new_field_farm_form.save()
        new_survey_field_form.save()

        return redirect("wisc_cc_survey3")
    # add form dictionary to context
    context["survey_farm_form"] = survey_farm_form
    context["survey_field_form"] = survey_field_form
    context["field_farm_form"] = field_farm_form
    template = "wisccc/survey_section_2.html"
    return render(request, template, context)


@login_required
def wisc_cc_survey3(request):
    # Don't forget to grab based on survey_year!!!
    survey_year = 2024
    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    survey_farm = (
        SurveyFarm.objects.filter(farmer_id=farmer.id)
        .filter(survey_year=survey_year)
        .first()
    )

    form = SurveyFarmFormPart3(request.POST or None, instance=survey_farm)

    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.farmer = farmer
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


@login_required
def deprecated_wisc_cc_survey1(request):
    try:
        # Survey.objects.get(farmer = Farmer.objects.get(user_id = 110))
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
def deprecated_wisc_cc_survey2(request):
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
def deprecated_wisc_cc_survey3(request):
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
    # retrieve signed url for accessing private s3 images
    # There is probably a better way to do this but while there aren't many
    #   submissions this is fine.
    for feat in data["features"]:
        if feat["properties"]["survey_field_id"]:
            survey_field_id = feat["properties"]["survey_field_id"]
        else:
            continue

        try:
            survey_photo = SurveyPhoto.objects.get(survey_field_id=survey_field_id)
        except SurveyPhoto.DoesNotExist:
            # print(f"Survey photo does not exist for {survey_field_id}")
            continue

        if survey_photo.image_1:
            feat["properties"]["image_1_url"] = survey_photo.image_1.url
        if survey_photo.image_2:
            feat["properties"]["image_2_url"] = survey_photo.image_2.url

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
            from wisccc_surveyfarm s 
            left join wisccc_farmer f
            on s.farmer_id = f.id 
            left join auth_user as u
            on f.user_id = u.id"""
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
def registration_table(request):
    """List wisc registration entries"""

    # all_regs = SurveyRegistration.objects.prefetch_related("farmer__user")
    def get_table_data():
        """For getting registration data"""
        query = """
            select
                ws.id
                , signup_timestamp
                , wf.farm_name
                , wf.first_name 
                , wf.last_name 
                , wf.address_zipcode
                , au.email
                , ws.belong_to_groups
                , ws.notes
                , howd_you_hear	
            from wisccc_surveyregistration ws 
            inner join wisccc_farmer wf 
            on ws.farmer_id = wf.id
            inner join auth_user au 
            on wf.user_id = au.id"""
        dat = pd.read_sql(query, connection)
        dat = dat.to_dict("records")

        return dat

    data = get_table_data()
    # total_regs = data.count()

    # table = ResponseTable(Survey.objects.all())
    table = RegistrationTable(data)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    return render(
        request,
        "wisccc/registration_table.html",
        {"table": table, "total_regs": 3},
    )


@permission_required("wisccc.survery_manager", raise_exception=True)
def update_registration(request, id):
    """For updating registration"""
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the survey object related to passed id
    registration = get_object_or_404(SurveyRegistration, id=id)

    # Get farmer associated with registrant
    farmer = registration.farmer

    # Get user associated with registrant
    user = registration.farmer.user

    # pass the object as instance in form
    registration_form = SurveyRegistrationFullForm(
        request.POST or None, instance=registration
    )

    farmer_form = FarmerForm(request.POST or None, instance=farmer)

    user_info_form = UserInfoForm(request.POST or None, instance=user)
    # save the data from the form and
    # redirect to detail_view

    if (
        registration_form.is_valid()
        and farmer_form.is_valid()
        and user_info_form.is_valid()
    ):

        registration_form.save()

        farmer_form.save()

        user_info_form.save()

        return redirect("registration_table")
    # add form dictionary to context
    context["registration_form"] = registration_form
    context["farmer_form"] = farmer_form
    context["user_info_form"] = user_info_form

    return render(request, "wisccc/wisc_cc_registration_review.html", context)


@permission_required("wisccc.survery_manager", raise_exception=True)
def delete_registration(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(SurveyRegistration, id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("registration_table")

    return render(request, "wisccc/delete_registration.html", context)


def get_registration_download():
    survey_registrants = (
        SurveyRegistration.objects.all()
        .select_related("farmer")
        .select_related("farmer__user")
    )

    df = pd.DataFrame(
        list(
            survey_registrants.values_list(
                # From registration
                "signup_timestamp",
                # From Farmer
                "farmer__id",
                # From User
                "farmer__user__email",
                "farmer__user__username",
                # From Farmer
                "farmer__first_name",
                "farmer__last_name",
                "farmer__farm_name",
                "farmer__county",
                "farmer__address_street",
                "farmer__address_municipality",
                "farmer__address_state",
                "farmer__address_zipcode",
                "farmer__phone_number",
                # From registration
                "survey_year",
                "biomass_or_just_survey",
                "do_you_have_a_biomas_kit",
                "do_you_need_assistance",
                "howd_you_hear",
                "belong_to_groups",
                "notes",
            )
        ),
        columns=[
            # From registration
            "signup_timestamp",
            # From Farmer
            "id",
            # From User
            "email",
            "username",
            # From Farmer
            "first_name",
            "last_name",
            "farm_name",
            "county",
            "street",
            "municipality",
            "state",
            "zipcode",
            "phone_number",
            # From registrants
            "survey_year",
            "biomass_or_just_survey",
            "do_you_have_a_biomas_kit",
            "do_you_need_assistance",
            "howd_you_hear",
            "belong_to_groups",
            "notes",
        ],
    )
    # convert farmer id to string, convert survey_year to string
    #   grab just the year and create and id
    df["id"] = (
        df["id"].apply(str).str.zfill(5) + "-" + df["survey_year"].apply(str).str[-2:]
    )
    df = df.drop("survey_year", axis=1)
    return df


@permission_required("wisccc.survery_manager", raise_exception=True)
def download_registrants(request):
    df = get_registration_download()
    filename = "registrants.csv"
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = f"attachment; filename={filename}"

    df.to_csv(path_or_buf=resp, sep=",", index=False)
    return resp


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

    # fetch the survey object related to passed id
    survey_farm = get_object_or_404(SurveyFarm, id=id)

    if survey_farm is None:
        survey_field = None
    else:
        survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()

    if survey_field is None:
        field_farm = None
    else:
        field_farm = FieldFarm.objects.filter(id=survey_field.field_farm_id).first()

    # Get farmer associated with user id of survey response
    farmer = Farmer.objects.filter(id=survey_farm.farmer_id).first()
    # Get any uploaded photos for this survey response
    survey_photo = SurveyPhoto.objects.filter(survey_field_id=survey_field.id).first()
    # pass the object as instance in form
    form_survey_farm = SurveyFarmFormFull(request.POST or None, instance=survey_farm)
    form_field_farm = FieldFarmFormFull(request.POST or None, instance=field_farm)
    form_survey_field = SurveyFieldFormFull(request.POST or None, instance=survey_field)
    form_farmer = FarmerForm(request.POST or None, instance=farmer)

    form_survey_photo = SurveyPhotoForm(request.POST or None, instance=survey_photo)
    # save the data from the form and
    # redirect to detail_view

    if (
        form_survey_farm.is_valid()
        and form_survey_field.is_valid()
        and form_field_farm.is_valid()
        and form_farmer.is_valid()
        and form_survey_photo.is_valid()
    ):

        form_survey_farm.save()
        form_survey_field.save()
        form_field_farm.save()
        # Here verify county
        # Here calc gdu?
        form_farmer.save()

        new_survey_photo = form_survey_photo.save()
        new_survey_photo.survey_field_id = survey_field.id
        if "image_1" in request.FILES.keys():
            new_survey_photo.image_1 = request.FILES["image_1"]
        if "image_2" in request.FILES.keys():
            new_survey_photo.image_2 = request.FILES["image_2"]

        new_survey_photo.save()

        return redirect("response_table")
    # add form dictionary to context
    context["farmer_form"] = form_farmer
    context["survey_farm_full_form"] = form_survey_farm
    context["survey_field_full_form"] = form_survey_field
    context["field_farm_full_form"] = form_field_farm

    context["survey_photo_form"] = form_survey_photo

    return render(request, "wisccc/survey_review.html", context)


def wisc_cc_signup(request):
    """For creating an account with wisc cc"""
    signup_form = CustomUserCreationForm(request.POST)
    if signup_form.is_valid():

        new_user = signup_form.save()
        auth_login(request, new_user)
        messages.success(request, "Account created successfully")
        return redirect("wisc_cc_home")

    return render(
        request,
        "wisccc/wisc_cc_signup.html",
        {"form": signup_form},
    )


def wisc_cc_register_1(request):
    """Registering for Wisc CC survey, assumes no previous account"""
    if request.user.id is not None:
        return redirect("wisc_cc_register_2")

    signup_form = CustomUserCreationForm(request.POST)
    if signup_form.is_valid():

        new_user = signup_form.save()
        auth_login(request, new_user)
        messages.success(request, "Account created successfully")
        return redirect("wisc_cc_register_2")

    return render(
        request,
        "wisccc/wisc_cc_register_1_signup.html",
        {"form": signup_form},
    )


@login_required
def wisc_cc_register_2(request):

    # TODO:
    #   Grab user info if they are logged in
    #   Grab farmer info if they are logged in and have a farmer attached to userid
    #   Grab registration info if they have already registered
    user = User.objects.get(id=request.user.id)
    try:
        farmer_instance = Farmer.objects.filter(user_id=request.user.id).first()
    except:
        farmer_instance = None

    farmer_form = FarmerForm(request.POST or None, instance=farmer_instance)

    try:
        registration_instance = SurveyRegistration.objects.filter(
            farmer_id=farmer_instance.id
        ).first()
    except:
        registration_instance = None

    registration_form = SurveyRegistrationPartialForm(
        request.POST or None, instance=registration_instance
    )

    if farmer_form.is_valid() and registration_form.is_valid():

        new_farmer = farmer_form.save(commit=False)
        new_register = registration_form.save(commit=False)

        new_farmer.user = user
        new_farmer.save()

        new_register.farmer = new_farmer
        new_register.survey_year = 2024
        new_register.save()

        messages.success(request, "Account created successfully")
        return redirect("wisc_cc_register_3")

    return render(
        request,
        "wisccc/wisc_cc_register_2.html",
        {
            "farmer_form": farmer_form,
            "registration_form": registration_form,
        },
    )


@login_required
def wisc_cc_register_3(request):

    return render(request, "wisccc/wisc_cc_register_3.html")


@permission_required("wisccc.survery_manager", raise_exception=True)
def upload_photo(request, id):
    """For uploading photos for survey response"""
    context = {}

    # Get any uploaded photos for this survey response

    survey_photo = SurveyPhoto.objects.filter(survey_response=id).first()

    survey_photo_form = SurveyPhotoForm(request.POST or None, instance=survey_photo)
    # save the data from the form and
    # redirect to detail_view

    if survey_photo_form.is_valid():

        new_survey_photo = survey_photo_form.save()
        new_survey_photo.survey_response_id = id
        if "image_1" in request.FILES.keys():
            new_survey_photo.image_1 = request.FILES["image_1"]
        if "image_2" in request.FILES.keys():
            new_survey_photo.image_2 = request.FILES["image_2"]

        new_survey_photo.save()

        return redirect("response_table")

    template = "wisccc/photo_upload.html"
    return render(
        request,
        template,
        {
            "survey_photo_form": survey_photo_form,
        },
    )
