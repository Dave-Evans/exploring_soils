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
from wisccc.derive_species_class import pull_all_years_together
import pandas as pd


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


def get_survey_data():
    """For getting survey data and returning an excel doc"""
    query = """
        select 
            s.user_id
            , s.id as response_id
            , u.username 
            , u.email
            , f.first_name 
            , f.last_name
            , f.farm_name  
            , f.county
            , st_x( farm_location ) as longitude
            , st_y( farm_location ) as latitude 
            , s.years_experience as "1. How many total years experience do you have planting cover crops?"
            , s.total_acres as "2. Total acres you planted to cover crops this year."
            , s.percent_of_farm_cc as "3. What percent of all your farm acres did you plant to covers this year?"
            , s.dominant_soil_series_1 as "4a. If you know the dominant soil series on your farm please list them below in order of how widely distributed. (ex. Plano, Drummer, Tama)."
            , s.dominant_soil_series_2 as "4b. Second most dominant"
            , s.dominant_soil_series_3 as "4c. Third most dominant"
            , s.dominant_soil_series_4 as "4d. Fourth most dominant"
            , s.info_source_nutrient_mgmt_1 as "5a. What are your top three sources of information for nutrient management?"
            , s.info_source_nutrient_mgmt_2 as "5b. Second"
            , s.info_source_nutrient_mgmt_3 as "5c. Third"
            , s.source_nutrient_mgmt_write_in as "6. If you chose other please explain."
            , s.cov_crops_for_ntrnt_mgmt_comments_questions as "7. Please share any experiences or questions regarding using cover crops for nutrient management."
            , s.info_source_cover_crops_1 as "8a. What are your top three sources of information on cover cropping?"
            , s.info_source_cover_crops_2 as "8b. Second"
            , s.info_source_cover_crops_3 as "8c. Third"
            , s.info_source_cover_crops_write_in as "9. If you chose social media or other please provide details."
            , s.support_cover_crops_1 as "10. Which of the following would make the biggest difference to you in terms of support for using cover crops?"
            , s.support_cover_crops_write_in as "11. If you chose “other” please provide details."
            , s.lacking_any_info_cover_crops as "12. Are you lacking in any information regarding cover crops? Please explain."
            , s.barriers_to_expansion as "13. Would you like to expand the number of acres you cover crop? If yes, what are the main barriers? Please share any details that will help us understand the challenges."
            , s.quit_planting_cover_crops as "14. What would it take for you to quit planting covers?"
            , s.if_use_crop_insurance as "15. Do you use crop insurance? If so, does it influence your cover cropping decisions, and how?"
            , s.why_cover_crops_write_in as "16. What are your top 3 motivations for cover cropping? Please explain."
            , s.closest_zip_code as "17. Enter the closest zip code for this field."
            , s.field_acreage as "18. What is this fields acreage?"
            , s.farm_location as "19. Zoom in to the map and click the general location for this field."
            , s.crop_rotation_2021_cash_crop_species as "20a. Cash crop planted 2021"
            , s.crop_rotation_2021_cover_crop_species as "20b. Cover crop planted in 2021"
            , s.crop_rotation_2022_cash_crop_species as "21a. Cash crop planted 2022"
            , s.crop_rotation_2022_cover_crop_species as "21b. Cover crop planted in 2022"
            , s.crop_rotation_2023_cash_crop_species as "22a. Cash crop planted 2023"
            , s.crop_rotation_2023_cover_crop_species as "22b. Cover crop planted in 2023"
            , s.crop_rotation as "23. Are there any other details you would like to share about your crop rotation?"
            , s.cover_crop_species_1 as "24a. Cover crop 1"
            , s.cover_crop_planting_rate_1 as "24b. Planting rate, for cover crop 1"
            , s.cover_crop_planting_rate_1_units as "24c. Units for cover crop 1"
            , s.cover_crop_species_2 as "25a. Cover crop 2"
            , s.cover_crop_planting_rate_2 as "25b. Planting rate, for cover crop 2"
            , s.cover_crop_planting_rate_2_units as "25c. Units for cover crop 2"
            , s.cover_crop_species_3 as "26a. Cover crop 3"
            , s.cover_crop_planting_rate_3 as "26b. Planting rate, for cover crop 3"
            , s.cover_crop_planting_rate_3_units as "26c. Units for cover crop 3"
            , s.cover_crop_species_4 as "27a. Cover crop 4"
            , s.cover_crop_planting_rate_4 as "27b. Planting rate, for cover crop 4"
            , s.cover_crop_planting_rate_4_units as "27c. Units for cover crop 4"
            , s.cover_crop_species_5 as "28a. Cover crop 5"
            , s.cover_crop_planting_rate_5 as "28b. Planting rate, for cover crop 5"
            , s.cover_crop_planting_rate_5_units as "28c. Units for cover crop 5"
            , s.cover_crop_species_and_rate_write_in as "29. Other cover crops planted and their rates, please specify in pounds per acre."
            , s.cover_crop_multispecies_mix_write_in as "30. If you planted a multispecies mix in 2023 please provide details."
            , s.cash_crop_planting_date as "31. What date this year did you plant your cash crop in this field? (Estimate is OK if not known)"
            , s.years_with_cover_crops as "32. How many years have you been planting cover crops *in this field*?"
            , s.dominant_soil_texture as "33. Please select the dominant soil texture of this field."
            , s.cover_crops_delay_cash_crop as "34. Does planting a cover crop delay when you would otherwise plant your cash crop?"
            , s.save_cover_crop_seed as "35. Do you save cover crop seed?"
            , s.source_cover_crop_seed as "36. What is your cover crop seed source?"
            , s.manure_prior as "37a. Will you apply manure prior to seeding cover crops on this field?"
            , s.manure_prior_rate as "37b. At what rate will the manure be applied?"
            , s.manure_prior_rate_units as "37c. Please select the units for the manure application rate."
            , s.manure_post as "38a. Will manure be applied to the field after the cover crop is established?"
            , s.manure_post_rate as "38b. At what rate will the manure be applied?"
            , s.manure_post_rate_units as "38c. Please select the units for the manure application rate."
            , s.tillage_system_cash_crop as "39. What is your tillage system for the cash crop preceding the cover crop?"
            , s.primary_tillage_equipment as "40. Primary tillage equipment (select all that apply) for a cash crop preceding a cover crop?"
            , s.primary_tillage_equipment_write_in as "40a. If you selected other, please explain."
            , s.secondary_tillage_equipment as "41a. Secondary tillage equipment (select all that apply) for cash crop preceding the cover crop?"
            , s.secondary_tillage_equipment_write_in as "41b. If you selected other, please explain."
            , s.soil_conditions_at_cover_crop_seeding as "42. Soil conditions in this field at cover crop seeding."
            , s.cover_crop_seeding_method as "43. Please select your the seeding method for your cover crop."
            , s.cover_crop_seeding_method_write_in as "43a. If you selected other, please explain."
            , s.cover_crop_seed_cost as "44. Estimated cover crop seed cost for this field ($/acre)"
            , s.cover_crop_planting_cost as "45. Estimated cover crop planting cost per acre in this field. Please use"
            , s.cover_crop_planting_date as "46. Cover crop planting date for this field (estimate is OK if not known)."
            , s.cover_crop_estimated_termination as "47. Estimated termination timing/method for this field."
            , s.days_between_crop_hvst_and_cc_estd as "48. Number of days estimated between crop harvest and cover crop establishment in this field."
            , s.interesting_tales as "49. Whats been your cover crop learning curve? Share any interesting experiments or failures."
            , s.where_to_start as "50. Where would you tell another grower to start with cover crops? Why?"
            , s.additional_thoughts as "51. Any additional thoughts or questions? Any important survey questions we should ask next time?"
            , s.survey_created
            , s.confirmed_accurate
            , s.notes_admin
            , s.derived_county
            , s.derived_species_class
            , labdata.*
        from wisccc_survey s 
        left join wisccc_farmer f
        on s.user_id = f.user_id 
        left join auth_user as u
        on s.user_id = u.id
        left join (
            select 
                id,
                COALESCE(
                   TO_DATE(lab.date_reported_biomass,'YYYY-MM-DD'),
                   TO_DATE(lab.date_processed,'YYYY-MM-DD')
                ) as cc_biomass_collection_date,
                cc_biomass,
                cp as fq_cp,
                andf as fq_andf,
                undfom30 as fq_undfom30,
                ndfd30 as fq_ndfd30,
                tdn_adf as fq_tdn_adf,
                milk_ton_milk2013 as fq_milkton,
                rfq as fq_rfq,
                total_precip,
                acc_gdd
            from all_lab_data_2023 lab 
        ) as labdata
        on s.id = labdata.id"""
    dat = pd.read_sql(query, connection)
    return dat


def check_user_has_registered(user_id):
    """For ensuring that the user has signed up prior
    to visiting the survey"""
    user = User.objects.filter(id=user_id).first()
    query = "select email from preregistered where email is not null"
    registered = pd.read_sql(query, connection).email.tolist()
    registered = [i.lower() for i in registered]
    b_registered = user.email.lower() in registered

    return b_registered


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

    # b_registered = check_user_has_registered(request.user.id)
    b_registered = True

    completed_0 = check_section_completed(request.user.id, "farmer")
    completed_1 = check_section_completed(request.user.id, 1)
    completed_2 = check_section_completed(request.user.id, 2)
    completed_3 = check_section_completed(request.user.id, 3)

    template = "wisccc/wisc_cc_survey.html"

    return render(
        request,
        template,
        {
            "b_registered": b_registered,
            "completed_0": completed_0,
            "completed_1": completed_1,
            "completed_2": completed_2,
            "completed_3": completed_3,
        },
    )


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
