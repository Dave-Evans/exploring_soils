import json
import djqscsv
import pandas as pd
import datetime
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import connection
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
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
from django_tables2 import RequestConfig, SingleTableMixin
from wisccc.tables import (
    ResponseTable,
    RegistrationTable,
    ResearcherTable,
    InterestedPartyTable,
    InterestedAgronomistTable,
)
from wisccc.filters import SurveyResponseFilter
from django_filters.views import FilterView
from wisccc.forms import (
    SurveyFieldFormFull,
    SurveyFarmFormSection2,
    FieldFarmFormSection3,
    SurveyFieldFormSection3,
    SurveyFarmFormSection4,
    SurveyFieldFormSection4_part1,
    SurveyFieldFormSection4_part2,
    SurveyFieldFormSection5,
    SurveyFieldFormSection6,
    SurveyFarmFormSection6,
    SurveyFarmFormSection7,
    SurveyFarmFormReview,
    FieldFarmFormFull,
    FarmerForm,
    SurveyFarmFormFull,
    SurveyPhotoForm,
    CustomUserCreationForm,
    SurveyRegistrationFullForm,
    SurveyRegistrationPartialForm,
    UserInfoForm,
    ResearcherSignupForm,
    ResearcherFullForm,
    AncillaryDataForm,
    SelectUserForm,
    InterestedPartyForm,
    InterestedAgronomistForm,
)
from wisccc.forms_2023 import (
    SurveyFarmFormPart1_2023,
    SurveyFarmFormPart2_2023,
    SurveyFieldFormFull_2023_parta,
    SurveyFieldFormFull_2023_partb,
    FieldFarmFormFull_2023,
    SurveyFarmFormPart3_2023,
)
from wisccc.models import (
    Survey,
    Farmer,
    SurveyPhoto,
    SurveyRegistration,
    SurveyField,
    SurveyFarm,
    FieldFarm,
    Researcher,
    AncillaryData,
    InterestedParty,
    InterestedAgronomist,
)
from wisccc.data_mgmt import (
    pull_all_years_together,
    get_survey_data,
    data_export,
    export_agronomic_data,
    get_registration_download,
    get_researchers_download,
)


# REVISE WITH NEW STRUCTURE
#   This will be dependent on how the forms shake out.
def check_section_completed(user_id, section):
    """Checks a particular section, farmer, 1, 2, 3
    to see if a particualr required field is a completed."""
    survey_year = 2024
    farmer = Farmer.objects.filter(user_id=user_id).first()
    if section == 1:

        if farmer is None:
            return False
        if farmer.last_name == "" or farmer.last_name is None:
            return False

        return True

    if section == 2:
        if farmer is None:
            return False
        survey_farm = (
            SurveyFarm.objects.filter(farmer_id=farmer.id)
            .filter(survey_year=survey_year)
            .first()
        )
        if survey_farm is None:
            return False
        if survey_farm.percent_of_farm_cc is None:
            return False

        return True

    if section == 3:
        if farmer is None:
            return False
        survey_farm = (
            SurveyFarm.objects.filter(farmer_id=farmer.id)
            .filter(survey_year=survey_year)
            .first()
        )
        if survey_farm is None:
            return False

        survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()
        if survey_field is None:
            return False

        if survey_field.crop_rotation_2023_cash_crop_species is None:
            return False

        return True

    if section == 4:
        if farmer is None:
            return False
        survey_farm = (
            SurveyFarm.objects.filter(farmer_id=farmer.id)
            .filter(survey_year=survey_year)
            .first()
        )
        if survey_farm is None:
            return False

        survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()
        if survey_field is None:
            return False

        if survey_field.cash_crop_planting_date is None:
            return False

        return True

    if section == 5:
        if farmer is None:
            return False
        survey_farm = (
            SurveyFarm.objects.filter(farmer_id=farmer.id)
            .filter(survey_year=survey_year)
            .first()
        )
        if survey_farm is None:
            return False

        survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()
        if survey_field is None:
            return False

        if survey_field.manure_post is None:
            return False

        return True

    if section == 6:
        if farmer is None:
            return False
        survey_farm = (
            SurveyFarm.objects.filter(farmer_id=farmer.id)
            .filter(survey_year=survey_year)
            .first()
        )
        if survey_farm is None:
            return False

        survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()
        if survey_field is None:
            return False

        if survey_field.cover_crop_seeding_method is None:
            return False

        return True

    if section == 7:
        if farmer is None:
            return False
        survey_farm = (
            SurveyFarm.objects.filter(farmer_id=farmer.id)
            .filter(survey_year=survey_year)
            .first()
        )
        if survey_farm is None:
            return False
        if (
            survey_farm.additional_thoughts is None
            and survey_farm.encourage_cc is None
            and survey_farm.encourage_cc_write_in is None
        ):
            return False

        return True


def wisc_cc_home(request):
    return render(request, "wisccc/wisc_cc_home.html")


@permission_required("wisccc.survery_manager", raise_exception=True)
def wisc_cc_manager_home(request):
    # Not ideal, but whenever a manager navigates to the admin home page
    #   approvals are checked
    check_researcher_approvals()

    return render(request, "wisccc/wisc_cc_manager_home.html")


def wisc_cc_about(request):
    return render(request, "wisccc/wisc_cc_about.html")


def wisc_cc_acis(request):
    return render(request, "wisccc/wisc_cc_acis.html")


def wisc_cc_clireg(request):
    return render(request, "wisccc/wisc_cc_clireg.html")


def wisc_cc_interested(request):

    form_interested_party = InterestedPartyForm(request.POST or None)
    # save the data from the form and
    # redirect to detail_view

    if form_interested_party.is_valid():
        form_interested_party.save()
        # new_form = form_interested_party.save(commit=False)
        # new_form.save()
        return redirect("wisc_cc_interested_thanks")

    return render(
        request,
        "wisccc/wisc_cc_interested.html",
        {"form_interested_party": form_interested_party},
    )


def wisc_cc_interested_thanks(request):
    return render(request, "wisccc/wisc_cc_interested_thanks.html")


@permission_required("wisccc.survery_manager", raise_exception=True)
def update_interested_party(request, id):
    """For updating interested party"""
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the survey object related to passed id
    interested_party = get_object_or_404(InterestedParty, id=id)

    # pass the object as instance in form
    form_interested_party = InterestedPartyForm(
        request.POST or None, instance=interested_party
    )

    # save the data from the form and
    # redirect to detail_view

    if form_interested_party.is_valid():

        form_interested_party.save()

        return redirect("interested_party_table")
    # add form dictionary to context
    context["form_interested_party"] = form_interested_party

    return render(request, "wisccc/wisc_cc_interested_review.html", context)


@permission_required("wisccc.survery_manager", raise_exception=True)
def delete_interested_party(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(InterestedParty, id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("interested_party_table")

    return render(request, "wisccc/delete_interested_party.html", context)


@permission_required("wisccc.survery_manager", raise_exception=True)
def interested_party_table(request):
    """List interested parties who have or have had access to download data"""

    def get_table_data():
        """For getting interested party data"""
        query = """
            select
                ip.id
                , ip.signup_timestamp
                , ip.first_name
                , ip.last_name
                , ip.email
                , ip.cover_crops_interest
                , ip.admin_notes
            from wisccc_interestedparty ip"""
        dat = pd.read_sql(query, connection)
        dat = dat.to_dict("records")

        return dat

    data = get_table_data()

    table = InterestedPartyTable(data)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    return render(
        request,
        "wisccc/interested_party_table.html",
        {"table": table},
    )


@permission_required("wisccc.survery_manager", raise_exception=True)
def wisccc_download_data(request, opt):
    # opt == 1 then full survey with qualitative
    # opt == 2 then display data
    if opt == 1:
        resp = HttpResponse(content_type="text/csv")
        filename = "full_survey_questions.csv"
        resp["Content-Disposition"] = f"attachment; filename={filename}"
        df = get_survey_data()
        df.to_csv(path_or_buf=resp, sep=",", index=False)
        return resp

    elif opt == 2:
        response = export_agronomic_data()
        return response

        export_name = "wisc_cc_data_export_{}.xlsx".format(
            datetime.datetime.now().strftime("%Y_%m_%d")
        )
        # filename = "cleaned_data_from_display.csv"
        # df.to_csv(path_or_buf=resp, sep=",", index=False)
        with open(filename, "rb") as f:
            resp = HttpResponse(f.read(), content_type="application/ms-excel")
            resp["Content-Disposition"] = f"attachment; filename={export_name}"

        return resp


@login_required
def wisc_cc_survey(request):
    """
    Home page for Cover Crop survey. We check progress of different sections of the survey
    by querying one required question from each section (0 (the farmer section),1,2,3).
    If this is completed then we assume it is all completed."""

    # Before we allow access to the survey page, user must
    #   be logged in ->
    #       -> Checked with decorator
    #   have a farmer entry
    #       -> Checked with Farmer.objects.get
    #   be registered for the proper survey season
    #       -> Check if user has registration record

    try:
        farmer_instance = Farmer.objects.get(user_id=request.user.id)
    except:
        return redirect("wisc_cc_register_1")

    try:
        registration = SurveyRegistration.objects.get(farmer_id=farmer_instance.id)
    except:
        return redirect("wisc_cc_register_1")

    completed_1 = check_section_completed(request.user.id, 1)
    completed_2 = check_section_completed(request.user.id, 2)
    completed_3 = check_section_completed(request.user.id, 3)
    completed_4 = check_section_completed(request.user.id, 4)
    completed_5 = check_section_completed(request.user.id, 5)
    completed_6 = check_section_completed(request.user.id, 6)
    completed_7 = check_section_completed(request.user.id, 7)

    template = "wisccc/wisc_cc_survey.html"

    return render(
        request,
        template,
        {
            "completed_1": completed_1,
            "completed_2": completed_2,
            "completed_3": completed_3,
            "completed_4": completed_4,
            "completed_5": completed_5,
            "completed_6": completed_6,
            "completed_7": completed_7,
        },
    )


@login_required
def wisc_cc_survey1(request):
    """I. General info: Farmer information"""
    try:
        instance = Farmer.objects.filter(user_id=request.user.id).first()
    except:
        instance = Farmer.objects.create(user_id=request.user.id)

    form_farmer = FarmerForm(request.POST or None, instance=instance)
    if form_farmer.is_valid():
        new_form = form_farmer.save(commit=False)
        new_form.user = request.user
        new_form.save()

        return redirect("wisc_cc_survey")

    template = "wisccc/survey_section_1_farmer.html"
    return render(
        request,
        template,
        {
            "form_farmer": form_farmer,
        },
    )


@login_required
def wisc_cc_survey2(request):
    """II. Cover cropping goals and support
    only Survey Farm data"""
    # field names as keys
    context = {}
    survey_year = 2024

    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    if farmer is None:
        # This is in case someone clicks to fill out the survey before filling in farmer info
        farmer = Farmer.objects.create(user_id=request.user.id)

    survey_farm = (
        SurveyFarm.objects.filter(farmer_id=farmer.id)
        .filter(survey_year=survey_year)
        .first()
    )
    # pass the object as instance in form
    form_surveyfarm_section_2 = SurveyFarmFormSection2(
        request.POST or None, instance=survey_farm
    )

    if form_surveyfarm_section_2.is_valid():
        new_form = form_surveyfarm_section_2.save(commit=False)
        new_form.farmer = farmer
        # Make sure to make a slot for this in the form.
        new_form.survey_year = survey_year
        new_form.save()

        return redirect("wisc_cc_survey3")

    template = "wisccc/survey_section_2_goals_support.html"
    return render(
        request, template, {"form_surveyfarm_section_2": form_surveyfarm_section_2}
    )


@login_required
def wisc_cc_survey3(request):
    """Research Field: Crop rotation and planting rates
    Uses SurveyField and FieldFarm
    We will redirect a user to separate page, where they will select
    either an existing field or opt to create a new one.
    They will be redirected this page if:
        survey_field (current survey year) does not have field_farm_id populated
        AND
        there is at least one field_farm object for that farmer
    """
    # field names as keys
    context = {}

    # Don't forget to grab based on survey_year!!!
    survey_year = 2024
    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    if farmer is None:
        # This is in case someone clicks to fill out the survey before filling in farmer info
        farmer = Farmer.objects.create(user_id=request.user.id)

    # Grab survey farm objects
    survey_farm = (
        SurveyFarm.objects.filter(farmer_id=farmer.id)
        .filter(survey_year=survey_year)
        .first()
    )

    # These if/else statements are here in case a record of the SurveyFarm is not yet created for 18.216.216.77
    # the farmer and needs to be created for this year. Without these if/else then errors occur because
    # of the need for the id field later on.
    if survey_farm is None:
        survey_farm = SurveyFarm.objects.create(farmer=farmer, survey_year=survey_year)
        survey_field = None
    else:
        survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()

    # If the survey field has not been created then no field populated for this year
    if survey_field is None:
        field_farm = None
    # If the field farm id is not null, then it has been populated already
    elif survey_field.field_farm_id is not None:
        field_farm = FieldFarm.objects.filter(id=survey_field.field_farm_id).first()
    else:
        field_farm = None
    print("field_farm is None", field_farm is None)
    # Is there a field_farm associated with this survey_field?
    if field_farm is None:
        # Check for fields associated with this farmer, if one or more, then send to selection page
        field_farms = FieldFarm.objects.filter(farmer_id=farmer.id)
        print("field_farms is None", field_farms is None)
        print("len(field_farms)", len(field_farms))
        if len(field_farms) >= 1:
            return redirect("wisc_cc_survey3a")
        # Else, then we will just be creating it here.

    # pass the object as instance in form
    form_surveyfield_section_3 = SurveyFieldFormSection3(
        request.POST or None, instance=survey_field
    )
    form_fieldfarm_section_3 = FieldFarmFormSection3(
        request.POST or None, instance=field_farm
    )

    if form_surveyfield_section_3.is_valid() and form_fieldfarm_section_3.is_valid():

        new_field_farm_form = form_fieldfarm_section_3.save(commit=False)
        new_field_farm_form.farmer = farmer
        new_survey_field_form = form_surveyfield_section_3.save(commit=False)
        new_survey_field_form.survey_farm = survey_farm
        new_survey_field_form.field_farm = new_field_farm_form
        # Make sure to save field_farm first
        new_field_farm_form.save()
        new_survey_field_form.save()

        return redirect("wisc_cc_survey4")
    # add form dictionary to context

    context["form_surveyfield_section_3"] = form_surveyfield_section_3
    context["form_fieldfarm_section_3"] = form_fieldfarm_section_3
    template = "wisccc/survey_section_3_field_rotation_rates.html"
    return render(request, template, context)


@login_required
def wisc_cc_survey3a(request):
    """For selecting which field the survey is for.
    We can assume that someone coming here has more than one.
    If no farmer associated, then send back to farmer part."""
    context = {}
    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    if farmer is None:
        return redirect("wisc_cc_survey1")

    field_farms = FieldFarm.objects.filter(farmer_id=farmer.id)
    context["field_farm_list"] = field_farms
    template = "wisccc/survey_section_3a_select_field.html"
    return render(request, template, context)


@login_required
def wisc_cc_survey4(request):
    """IV. Research Field: Planting dates & timing
    Uses survey_field and one question, cash crop planting date, from surveyfarm"""
    # Don't forget to grab based on survey_year!!!
    survey_year = 2024
    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    if farmer is None:
        # This is in case someone clicks to fill out the survey before filling in farmer info
        farmer = Farmer.objects.create(user_id=request.user.id)
    survey_farm = (
        SurveyFarm.objects.filter(farmer_id=farmer.id)
        .filter(survey_year=survey_year)
        .first()
    )
    if survey_farm is None:
        survey_farm = SurveyFarm.objects.create(farmer=farmer, survey_year=survey_year)
        survey_field = None
    else:
        survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()

    form_surveyfarm_section_4 = SurveyFarmFormSection4(
        request.POST or None, instance=survey_farm
    )
    form_surveyfield_section_4_part_1 = SurveyFieldFormSection4_part1(
        request.POST or None, instance=survey_field
    )
    form_surveyfield_section_4_part_2 = SurveyFieldFormSection4_part2(
        request.POST or None, instance=survey_field
    )

    if (
        form_surveyfarm_section_4.is_valid()
        and form_surveyfield_section_4_part_1.is_valid()
        and form_surveyfield_section_4_part_2.is_valid()
    ):

        new_survey_farm_form = form_surveyfarm_section_4.save(commit=False)
        new_survey_farm_form.farmer = farmer
        new_survey_farm_form.survey_year = survey_year
        new_survey_farm_form.save()
        new_form_survey_field_part_1 = form_surveyfield_section_4_part_1.save(
            commit=False
        )
        new_form_survey_field_part_1.survey_farm = survey_farm
        new_form_survey_field_part_1.save()
        new_form_survey_field_part_2 = form_surveyfield_section_4_part_2.save(
            commit=False
        )
        new_form_survey_field_part_2.survey_farm = survey_farm
        new_form_survey_field_part_2.save()

        return redirect("wisc_cc_survey5")

    template = "wisccc/survey_section_4_field_planting_dates_timing.html"
    return render(
        request,
        template,
        {
            "form_surveyfarm_section_4": form_surveyfarm_section_4,
            "form_surveyfield_section_4_part_1": form_surveyfield_section_4_part_1,
            "form_surveyfield_section_4_part_2": form_surveyfield_section_4_part_2,
        },
    )


@login_required
def wisc_cc_survey5(request):
    """V. Research Field: Manure, tillage, soil conditions
    Uses SurveyField"""
    # field names as keys
    context = {}

    # Don't forget to grab based on survey_year!!!
    survey_year = 2024
    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    if farmer is None:
        # This is in case someone clicks to fill out the survey before filling in farmer info
        farmer = Farmer.objects.create(user_id=request.user.id)
    survey_farm = (
        SurveyFarm.objects.filter(farmer_id=farmer.id)
        .filter(survey_year=survey_year)
        .first()
    )
    if survey_farm is None:
        survey_farm = SurveyFarm.objects.create(farmer=farmer, survey_year=survey_year)
        survey_field = None
    else:
        survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()

    # pass the object as instance in form
    form_surveyfield_section_5 = SurveyFieldFormSection5(
        request.POST or None, instance=survey_field
    )

    if form_surveyfield_section_5.is_valid():

        new_survey_field_form = form_surveyfield_section_5.save(commit=False)
        new_survey_field_form.survey_farm = survey_farm
        new_survey_field_form.save()

        return redirect("wisc_cc_survey6")
    # add form dictionary to context

    context["form_surveyfield_section_5"] = form_surveyfield_section_5
    template = "wisccc/survey_section_5_field_tillage_manure_soil.html"
    return render(request, template, context)


@login_required
def wisc_cc_survey6(request):
    """VI. Research Field: Cover crop seeding & cost
    Uses survey_field and surveyfarm"""
    # Don't forget to grab based on survey_year!!!
    survey_year = 2024
    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    if farmer is None:
        # This is in case someone clicks to fill out the survey before filling in farmer info
        farmer = Farmer.objects.create(user_id=request.user.id)
    survey_farm = (
        SurveyFarm.objects.filter(farmer_id=farmer.id)
        .filter(survey_year=survey_year)
        .first()
    )
    if survey_farm is None:
        survey_farm = SurveyFarm.objects.create(farmer=farmer, survey_year=survey_year)
        survey_field = None
    else:
        survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()

    form_surveyfarm_section_6 = SurveyFarmFormSection6(
        request.POST or None, instance=survey_farm
    )
    form_surveyfield_section_6 = SurveyFieldFormSection6(
        request.POST or None, instance=survey_field
    )

    if form_surveyfarm_section_6.is_valid() and form_surveyfield_section_6.is_valid():

        new_form_survey_farm = form_surveyfarm_section_6.save(commit=False)
        new_form_survey_farm.farmer = farmer
        new_form_survey_farm.survey_year = survey_year
        new_form_survey_farm.save()
        new_form_survey_field = form_surveyfield_section_6.save(commit=False)
        new_form_survey_field.survey_farm = survey_farm
        new_form_survey_field.save()

        return redirect("wisc_cc_survey7")

    template = "wisccc/survey_section_6_field_seeding_cost.html"
    return render(
        request,
        template,
        {
            "form_surveyfarm_section_6": form_surveyfarm_section_6,
            "form_surveyfield_section_6": form_surveyfield_section_6,
        },
    )


@login_required
def wisc_cc_survey7(request):
    """VII. Final thoughts
    Uses SurveyFarm"""
    context = {}
    survey_year = 2024

    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    if farmer is None:
        # This is in case someone clicks to fill out the survey before filling in farmer info
        farmer = Farmer.objects.create(user_id=request.user.id)

    survey_farm = (
        SurveyFarm.objects.filter(farmer_id=farmer.id)
        .filter(survey_year=survey_year)
        .first()
    )

    # pass the object as instance in form
    form_surveyfarm_section_7 = SurveyFarmFormSection7(
        request.POST or None, instance=survey_farm
    )

    if form_surveyfarm_section_7.is_valid():
        new_form_surveyfarm_section_7 = form_surveyfarm_section_7.save(commit=False)
        new_form_surveyfarm_section_7.farmer = farmer
        new_form_surveyfarm_section_7.survey_year = survey_year
        new_form_surveyfarm_section_7.save()

        return redirect("wisc_cc_survey")

    template = "wisccc/survey_section_7_final_thoughts.html"
    return render(
        request, template, {"form_surveyfarm_section_7": form_surveyfarm_section_7}
    )


@permission_required("wisccc.survery_manager", raise_exception=True)
def update_labdata(request, id):
    """For updating labdata
    Will navigate to this page via the survey table
    page so will use SurveyFarm id to grab ancillary data
    """
    context = {}
    survey_farm = get_object_or_404(SurveyFarm, id=id)
    first_and_last_name = (
        f"{survey_farm.farmer.first_name} {survey_farm.farmer.last_name}"
    )
    survey_year = f"{survey_farm.survey_year}"

    survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()
    # Get any lab data for this survey response
    ancillary_data = AncillaryData.objects.filter(
        survey_field_id=survey_field.id
    ).first()

    form_ancillary_data = AncillaryDataForm(
        request.POST or None, instance=ancillary_data
    )
    if form_ancillary_data.is_valid():

        new_ancillary_data = form_ancillary_data.save()
        new_ancillary_data.survey_field_id = survey_field.id

        new_ancillary_data.save()

        return redirect("response_table")

    template = "wisccc/wisc_cc_ancillarydata_review.html"
    return render(
        request,
        template,
        {
            "form": form_ancillary_data,
            "first_and_last_name": first_and_last_name,
            "survey_year": survey_year,
        },
    )


@permission_required("wisccc.survery_manager", raise_exception=True)
def update_response(request, id):
    """For updating survey"""
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the survey object related to passed id
    survey_farm = get_object_or_404(SurveyFarm, id=id)

    # Get farmer associated with user id of survey response
    farmer = Farmer.objects.filter(id=survey_farm.farmer_id).first()
    first_and_last_name = f"{farmer.first_name} {farmer.last_name}"
    # Is there a survey field record for this survey?
    #   if so grab it, else create one
    survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()
    if survey_field is None:
        survey_field = SurveyField.objects.create(survey_farm_id=survey_farm.id)

    # Is there a field farm record for this survey?
    #   if so grab it, else create one
    field_farm = FieldFarm.objects.filter(id=survey_field.field_farm_id).first()
    if field_farm is None:
        field_farm = FieldFarm.objects.create(farmer=farmer)
        survey_field.field_farm = field_farm
        survey_field.save()
    # Is there a Survey photo record for this survey?
    #   if so grab it, else create one
    survey_photo = SurveyPhoto.objects.filter(survey_field_id=survey_field.id).first()
    if survey_photo is None:
        survey_photo = SurveyPhoto.objects.create(survey_field=survey_field)

    # pass the object as instance in form
    # Section 1 - Farmer
    form_farmer_section_1 = FarmerForm(request.POST or None, instance=farmer)
    # Get any uploaded photos for this survey response
    form_survey_photo = SurveyPhotoForm(request.POST or None, instance=survey_photo)
    # Review questions: Confirm accurate and Notes
    form_surveyfarm_review = SurveyFarmFormReview(
        request.POST or None, instance=survey_farm
    )

    form_context = {
        "form_farmer": form_farmer_section_1,
        "form_surveyfarm_review": form_surveyfarm_review,
        "survey_photo_form": form_survey_photo,
    }
    if survey_farm.survey_year == 2023:

        # Section 1
        #   wisccc/includes/form_survey_part_1.html
        form_surveyfarm_section_1 = SurveyFarmFormPart1_2023(
            request.POST or None, instance=survey_farm
        )
        # Section 2
        #   wisccc/includes/form_survey_part_2_fieldfarm.html
        #   wisccc/includes/form_survey_part_2_surveyfield.html
        #   wisccc/includes/form_survey_part_2_surveyfarm.html
        form_surveyfarm_section_2 = SurveyFarmFormPart2_2023(
            request.POST or None, instance=survey_farm
        )
        form_surveyfield_section_2_part_a = SurveyFieldFormFull_2023_parta(
            request.POST or None, instance=survey_field
        )
        form_surveyfield_section_2_part_b = SurveyFieldFormFull_2023_partb(
            request.POST or None, instance=survey_field
        )
        form_fieldfarm_section_2 = FieldFarmFormFull_2023(
            request.POST or None, instance=field_farm
        )
        # Section 3
        #   wisccc/includes/form_survey_part_3.html
        form_surveyfarm_section_3 = SurveyFarmFormPart3_2023(
            request.POST or None, instance=survey_farm
        )
        form_context["form_surveyfarm_section_1"] = form_surveyfarm_section_1
        form_context["form_surveyfarm_section_2"] = form_surveyfarm_section_2
        form_context["form_surveyfield_section_2_part_a"] = (
            form_surveyfield_section_2_part_a
        )
        form_context["form_surveyfield_section_2_part_b"] = (
            form_surveyfield_section_2_part_b
        )
        form_context["form_fieldfarm_section_2"] = form_fieldfarm_section_2
        form_context["form_surveyfarm_section_3"] = form_surveyfarm_section_3
        # 2023 template
        template = "wisccc/survey_review_2023.html"
    elif survey_farm.survey_year == 2024:
        # Section 2 - SurveyFarm
        form_surveyfarm_section_2 = SurveyFarmFormSection2(
            request.POST or None, instance=survey_farm
        )

        # Section 3 - SurveyField and FarmField
        form_surveyfield_section_3 = SurveyFieldFormSection3(
            request.POST or None, instance=survey_field
        )
        form_fieldfarm_section_3 = FieldFarmFormSection3(
            request.POST or None, instance=field_farm
        )
        # Section 4 - SurveyFarm and SurveyField
        form_surveyfield_section_4_part_1 = SurveyFieldFormSection4_part1(
            request.POST or None, instance=survey_field
        )
        form_surveyfarm_section_4 = SurveyFarmFormSection4(
            request.POST or None, instance=survey_farm
        )
        form_surveyfield_section_4_part_2 = SurveyFieldFormSection4_part2(
            request.POST or None, instance=survey_field
        )
        # Section 5 - SurveyField
        form_surveyfield_section_5 = SurveyFieldFormSection5(
            request.POST or None, instance=survey_field
        )
        # Section 6 - SurveyFarm and SurveyField
        form_surveyfarm_section_6 = SurveyFarmFormSection6(
            request.POST or None, instance=survey_farm
        )
        form_surveyfield_section_6 = SurveyFieldFormSection6(
            request.POST or None, instance=survey_field
        )
        # Section 7 - SurveyFarm
        form_surveyfarm_section_7 = SurveyFarmFormSection7(
            request.POST or None, instance=survey_farm
        )
        # For making all review questions NOT required
        form_context["form_surveyfarm_section_2"] = form_surveyfarm_section_2
        form_context["form_surveyfield_section_3"] = form_surveyfield_section_3
        form_context["form_fieldfarm_section_3"] = form_fieldfarm_section_3
        form_context["form_surveyfield_section_4_part_1"] = (
            form_surveyfield_section_4_part_1
        )
        form_context["form_surveyfarm_section_4"] = form_surveyfarm_section_4
        form_context["form_surveyfield_section_4_part_2"] = (
            form_surveyfield_section_4_part_2
        )
        form_context["form_surveyfield_section_5"] = form_surveyfield_section_5
        form_context["form_surveyfarm_section_6"] = form_surveyfarm_section_6
        form_context["form_surveyfield_section_6"] = form_surveyfield_section_6
        form_context["form_surveyfarm_section_7"] = form_surveyfarm_section_7
        # 2024 template
        template = "wisccc/survey_review_2024.html"

    # Make everything not required for the review
    for frm in form_context:
        for fld in form_context[frm].fields:
            form_context[frm].fields[fld].required = False

    # save the data from the form and
    # redirect to detail_view

    if all([form_context[frm].is_valid() for frm in form_context]):

        for frm in form_context:
            if frm == "survey_photo_form":

                new_survey_photo = form_context["survey_photo_form"].save()
                new_survey_photo.survey_field_id = survey_field.id
                if "image_1" in request.FILES.keys():
                    new_survey_photo.image_1 = request.FILES["image_1"]
                if "image_2" in request.FILES.keys():
                    new_survey_photo.image_2 = request.FILES["image_2"]

                new_survey_photo.save()
            else:
                form_context[frm].save()

        return redirect("response_table")

    form_context["first_and_last_name"] = first_and_last_name
    return render(request, template, form_context)


@login_required
def update_fieldfarm(request, id):
    """Takes field_farm id"""
    context = {}
    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    if farmer is None:
        redirect("wisc_cc_survey1")

    # Verify they can do this, better with perms.
    field_farms = FieldFarm.objects.filter(farmer_id=farmer.id)
    if id not in field_farms:
        print("You don't have access to this field!")

    field_farm = get_object_or_404(FieldFarm, id=id)
    form_field_farm = FieldFarmFormFull(request.POST or None, instance=field_farm)
    # save the data from the form and
    # redirect to detail_view

    if form_field_farm.is_valid():

        new_field_farm_form = form_field_farm.save(commit=False)
        new_field_farm_form.farmer = farmer
        new_field_farm_form.save()

        return redirect("wisc_cc_survey3")
    # add form dictionary to context
    context["field_farm_full_form"] = form_field_farm
    context["field_farm"] = field_farm

    return render(request, "wisccc/fieldfarm_update.html", context)


@login_required
def create_fieldfarm(request):
    """Takes field_farm id"""
    survey_year = 2024
    context = {}
    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    if farmer is None:
        redirect("wisc_cc_survey1")

    form_field_farm = FieldFarmFormFull(request.POST or None)
    # save the data from the form and
    # redirect to detail_view

    if form_field_farm.is_valid():

        new_field_farm_form = form_field_farm.save(commit=False)
        new_field_farm_form.farmer = farmer
        new_field_farm_form.save()

        # If creating a field, we are assuming that this is the field the farmer
        # wants to fill out the survey for

        return redirect(f"wisc_cc_survey_populate_fieldfarm/{new_field_farm_form.id}")
    # add form dictionary to context
    context["field_farm_full_form"] = form_field_farm

    return render(request, "wisccc/fieldfarm_create.html", context)


@login_required
def wisc_cc_survey_populate_fieldfarm(request, id):
    """Update the current years survey (field)
    with this fieldfarm id"""
    print("We are in populate!")
    survey_year = 2024
    farmer = Farmer.objects.filter(user_id=request.user.id).first()
    # Grab survey farm objects
    survey_farm = (
        SurveyFarm.objects.filter(farmer_id=farmer.id)
        .filter(survey_year=survey_year)
        .first()
    )

    # These if/else statements are here in case a record of the SurveyFarm is not yet created for 18.216.216.77
    # the farmer and needs to be created for this year. Without these if/else then errors occur because
    # of the need for the id field later on.
    print("Survey farm is None?", survey_farm is None)
    if survey_farm is None:
        survey_farm = SurveyFarm.objects.create(farmer=farmer, survey_year=survey_year)
        survey_field = SurveyField.objects.create(survey_farm_id=survey_farm.id)
    else:
        survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()

    print("Survey field is None?", survey_field is None)
    if survey_field is None:
        survey_field = SurveyField.objects.create(survey_farm_id=survey_farm.id)

    print("Farmfield id:", id)
    survey_field.field_farm_id = id
    survey_field.save()

    return redirect("wisc_cc_survey3")


def wisc_cc_graph(request):
    return render(request, "wisccc/wisc_cc_graph.html")


def wisc_cc_map(request):
    return render(request, "wisccc/wisc_cc_map.html")


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
            feat["properties"]["caption_photo_1"] = survey_photo.caption_photo_1
        if survey_photo.image_2:
            feat["properties"]["image_2_url"] = survey_photo.image_2.url
            feat["properties"]["caption_photo_2"] = survey_photo.caption_photo_2

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


@permission_required("wisccc.survery_manager", raise_exception=True)
def wisccc_create_researcher(request):
    """For creating a new researcher
    Currently this assumes we are creating a *new user*
    This may not always be the case. How to allow manager to
    populate user info by looking up existing email addresses?
    """

    researcher_form = ResearcherSignupForm(request.POST or None)

    client_ip = request.META.get("REMOTE_ADDR")
    signup_form = CustomUserCreationForm(
        request.POST or None, initial={"client_ip": client_ip}
    )

    signup_form.fields["turnstile"].required = True
    signup_form.fields["turnstile"].client_ip = client_ip

    if researcher_form.is_valid() and signup_form.is_valid():

        new_researcher = researcher_form.save(commit=False)
        new_user = signup_form.save(commit=False)

        new_researcher.user = new_user
        if new_researcher.approved:
            content_type = ContentType.objects.get_for_model(Researcher)
            perm_approved_researcher = Permission.objects.get(
                codename="approved_researcher"
            )
            new_researcher.approved_date = datetime.date.today()
            new_user.user_permissions.add(perm_approved_researcher)
        new_researcher.save()
        new_user.save()

        return redirect("researcher_table")
    else:
        return render(
            request,
            "wisccc/wisc_cc_create_researcher.html",
            {
                "researcher_form": researcher_form,
                # Uses a generic form
                "form": signup_form,
            },
        )


@permission_required("wisccc.survery_manager", raise_exception=True)
def wisccc_create_researcher_existing_user(request):
    """For creating a new researcher
    This assumes we are creating a researcher for an existing user.
    """

    researcher_form = ResearcherSignupForm(request.POST or None)

    select_form = SelectUserForm(request.POST or None)

    if researcher_form.is_valid() and select_form.is_valid():

        new_researcher = researcher_form.save(commit=False)
        # Form returns a queryset, so we select the first object, there is only one
        # print(select_form.cleaned_data)

        new_user = User.objects.get(id=select_form.cleaned_data["user_select"])

        new_researcher.user = new_user
        if new_researcher.approved:
            content_type = ContentType.objects.get_for_model(Researcher)
            perm_approved_researcher = Permission.objects.get(
                codename="approved_researcher"
            )
            new_researcher.approved_date = datetime.date.today()
            new_user.user_permissions.add(perm_approved_researcher)
        new_researcher.save()
        new_user.save()

        return redirect("researcher_table")
    else:
        return render(
            request,
            "wisccc/wisc_cc_create_researcher_existing_user.html",
            {
                "researcher_form": researcher_form,
                # Uses a generic form
                "form": select_form,
            },
        )


def researcher_page(request):

    # if user has the permission then allow them to see the download page,
    #   otherwise redirect to a page explaining the process to get approved
    if not request.user.has_perm(
        "wisccc.approved_researcher"
    ) and not request.user.has_perm("wisccc.survery_manager"):

        return redirect("researcher_page_unapproved")

    return render(request, "wisccc/wisc_cc_researcher.html")


def researcher_page_unapproved(request):

    return render(request, "wisccc/wisc_cc_researcher_unapproved.html")


@permission_required("wisccc.survery_manager", raise_exception=True)
def researcher_table(request):
    """List researchers who have or have had access to download data"""

    def get_table_data():
        """For getting researcher data"""
        query = """
            select
                wr.id
                , wr.first_name
                , wr.last_name
                , au.email
                , au.username
                , wr.signup_timestamp
                , wr.institution
                , wr.agreement_doc
                , wr.notes
                , wr.approved
                , wr.approved_date
                , wr.download_count
                , wr.last_download_timestamp
            from wisccc_researcher wr 
            inner join auth_user au 
            on wr.user_id = au.id"""
        dat = pd.read_sql(query, connection)
        dat = dat.to_dict("records")

        return dat

    data = get_table_data()

    table = ResearcherTable(data)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    return render(
        request,
        "wisccc/researcher_table.html",
        {"table": table},
    )


@permission_required("wisccc.survery_manager", raise_exception=True)
def delete_researcher(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Researcher, id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("researcher_table")

    return render(request, "wisccc/delete_researcher.html", context)


@permission_required("wisccc.survery_manager", raise_exception=True)
def update_researcher(request, id):
    """For updating researcher"""
    # dictionary for initial data with
    # field names as keys
    context = {}
    content_type = ContentType.objects.get_for_model(Researcher)
    perm_approved_researcher = Permission.objects.get(codename="approved_researcher")
    # fetch the survey object related to passed id
    researcher = get_object_or_404(Researcher, id=id)
    initial_approved_status = researcher.approved
    # Get user associated with registrant
    user = researcher.user

    # pass the object as instance in form
    researcher_form = ResearcherFullForm(request.POST or None, instance=researcher)

    user_info_form = UserInfoForm(request.POST or None, instance=user)
    # save the data from the form and
    # redirect to detail_view

    if researcher_form.is_valid() and user_info_form.is_valid():

        new_user_info_form = user_info_form.save(commit=False)
        new_researcher_form = researcher_form.save(commit=False)
        if new_researcher_form.approved:
            # For the case when going from not approved to approved,
            # we reset the date
            if initial_approved_status == False:
                new_researcher_form.approved_date = datetime.date.today()
                new_user_info_form.user_permissions.add(perm_approved_researcher)
                new_user_info_form.save()
                # Refetch to update the perms
                user = User.objects.get(id=researcher.id)
        else:
            # When intially approved then approval revoked, nullify date
            if initial_approved_status == True:
                new_researcher_form.approved_date = None
                new_user_info_form.user_permissions.remove(perm_approved_researcher)
                new_user_info_form.save()
                # Refetch to update the perms
                user = User.objects.get(id=researcher.id)
        if "agreement_doc" in request.FILES.keys():
            new_researcher_form.agreement_doc = request.FILES["agreement_doc"]
        new_researcher_form.save()
        return redirect("researcher_table")
    # add form dictionary to context
    context["researcher_form"] = researcher_form
    context["user_info_form"] = user_info_form

    return render(request, "wisccc/wisc_cc_researcher_review.html", context)


@permission_required("wisccc.approved_researcher", raise_exception=True)
def wisccc_researcher_download_data(request):
    researcher_instance = Researcher.objects.get(user_id=request.user.id)
    # run test for if expired
    if abs(researcher_instance.approved_date - datetime.date.today()).days > 366:
        return redirect("researcher_page_expired")

    response = export_agronomic_data()
    researcher_instance.download_count += 1
    researcher_instance.last_download_timestamp = datetime.datetime.now()
    researcher_instance.save()
    return response


def check_researcher_approvals():

    researchers = Researcher.objects.all()
    for researcher in researchers:
        # If the approval was given more than 366 days ago, set
        #   approved to False
        if researcher.approved_date is None:
            continue
        if abs(researcher.approved_date - datetime.date.today()).days > 366:
            researcher.approved = False
            researcher.save()


def researcher_page_expired(request):

    return render(request, "wisccc/wisc_cc_researcher_expired.html")


# @permission_required("wisccc.survery_manager", raise_exception=True)
# @method_decorator(permission_required, name="dispatch")
class ResponseTableListView(SingleTableMixin, FilterView):
    """List survey responses, with filters"""

    table_class = ResponseTable
    model = SurveyFarm
    template_name = "wisccc/response_table.html"

    filterset_class = SurveyResponseFilter

    def get_queryset(self):
        return super().get_queryset().filter(survey_year__gt=2022)

    # def get_table_kwargs(self):
    #     return {"template_name": "django_tables2/bootstrap.html"}


@permission_required("wisccc.survery_manager", raise_exception=True)
def response_table_bkup(request):
    """List wisc response entries"""
    all_surveys = (
        SurveyFarm.objects.select_related("farmer")
        .select_related("farmer__user")
        .filter(survey_year__gt=2022)
    )
    total_surveys = all_surveys.count()
    completed_surveys = (
        all_surveys.filter(percent_of_farm_cc__isnull=False)
        .filter(save_cover_crop_seed__isnull=False)
        .filter(additional_thoughts__isnull=False)
        .count()
    )

    table = ResponseTable(all_surveys)
    filter = SurveyResponseFilter(request.GET, queryset=all_surveys)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    return render(
        request,
        "wisccc/response_table.html",
        {
            "table": table,
            "total_surveys": total_surveys,
            "completed_surveys": completed_surveys,
            "filter": filter,
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
    context["form_farmer"] = farmer_form
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


@permission_required("wisccc.survery_manager", raise_exception=True)
def download_registrants(request):
    df = get_registration_download()
    filename = "registrants.csv"
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = f"attachment; filename={filename}"

    df.to_csv(path_or_buf=resp, sep=",", index=False)
    return resp


@permission_required("wisccc.survery_manager", raise_exception=True)
def download_researchers(request):
    df = get_researchers_download()

    filename = "researchers_{}.csv".format(datetime.datetime.now().strftime("%Y_%m_%d"))
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
    obj = get_object_or_404(SurveyFarm, id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect back to
        # reponse table
        return redirect("response_table")

    return render(request, "wisccc/delete_response.html", context)


def wisc_cc_signup(request):
    """For creating an account with wisc cc"""
    client_ip = request.META.get("REMOTE_ADDR")
    signup_form = CustomUserCreationForm(
        request.POST or None, initial={"client_ip": client_ip}
    )
    signup_form.fields["turnstile"].required = True
    signup_form.fields["turnstile"].client_ip = client_ip

    if request.method == "POST":
        if signup_form.is_valid():

            new_user = signup_form.save()
            auth_login(request, new_user)
            messages.success(request, "Account created successfully")
            return redirect("wisc_cc_home")

        else:
            # print("here's the errors:")
            # for err in signup_form.errors:
            #     print(err)
            #     print(type(err))

            return render(
                request,
                "wisccc/wisc_cc_signup.html",
                {"form": signup_form},
            )

    return render(
        request,
        "wisccc/wisc_cc_signup.html",
        {"form": signup_form},
    )


def wisc_cc_register_1(request):
    """Registering for Wisc CC survey, assumes no previous account"""
    if request.user.id is not None:
        return redirect("wisc_cc_register_2")

    client_ip = request.META.get("REMOTE_ADDR")
    signup_form = CustomUserCreationForm(
        request.POST or None, initial={"client_ip": client_ip}
    )
    signup_form.fields["turnstile"].required = True
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
    """For when a user already exists."""
    user = User.objects.get(id=request.user.id)

    farmer_instance = Farmer.objects.filter(user_id=request.user.id).first()

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
            "form_farmer": farmer_form,
            "registration_form": registration_form,
        },
    )


@permission_required("wisccc.survery_manager", raise_exception=True)
def wisc_cc_register_by_mgmt_exist_user_select(request):
    """For when a registrant is signed up by survey manager
    This is for when the user already exists in our system.
    This first page is for just selecting the user.
    """
    survey_year = 2024

    select_user_form = SelectUserForm(request.POST or None)

    if select_user_form.is_valid():

        # selected_user = User.objects.get(id=select_user_form.cleaned_data["user_select"])

        return redirect(
            "wisc_cc_register_by_mgmt_exist_user",
            pk=select_user_form.cleaned_data["user_select"],
        )
    else:
        return render(
            request,
            "wisccc/wisc_cc_register_by_mgmt_exist_user_select.html",
            {
                "form": select_user_form,
            },
        )


@permission_required("wisccc.survery_manager", raise_exception=True)
def wisc_cc_register_by_mgmt_exist_user(request, pk):
    """For when a registrant is signed up by survey manager
    This is for when the user already exists in our system.
    This page is for when the user has been selected. The id here is the user id.
    """
    survey_year = 2024

    selected_user = get_object_or_404(User, id=pk)
    try:
        farmer_instance = Farmer.objects.filter(user_id=selected_user.id).first()
    except:
        farmer_instance = Farmer.objects.create(user_id=selected_user.id)

    form_farmer = FarmerForm(request.POST or None, instance=farmer_instance)

    registration_instance = SurveyRegistration.objects.filter(
        farmer=farmer_instance
    ).first()
    registration_form = SurveyRegistrationFullForm(
        request.POST or None, instance=registration_instance
    )

    if registration_form.is_valid() and form_farmer.is_valid():

        new_farmer = form_farmer.save(commit=False)
        new_registrant = registration_form.save(commit=False)

        new_farmer.user = selected_user
        new_farmer.save()

        new_registrant.farmer = new_farmer
        new_registrant.survey_year = survey_year

        new_registrant.save()

        return redirect("registration_table")
    else:
        return render(
            request,
            "wisccc/wisc_cc_register_by_mgmt_exist_user.html",
            {
                "registration_form": registration_form,
                "form_farmer": form_farmer,
                "selected_user": selected_user,
            },
        )


@permission_required("wisccc.survery_manager", raise_exception=True)
def wisc_cc_register_by_mgmt(request):
    """For when a registrant is signed up by survey manager
    This is for when the user is new.
    """
    survey_year = 2024
    client_ip = request.META.get("REMOTE_ADDR")

    registration_form = SurveyRegistrationFullForm(request.POST or None)
    farmer_form = FarmerForm(request.POST or None)

    signup_form = CustomUserCreationForm(
        request.POST or None, initial={"client_ip": client_ip}
    )

    signup_form.fields["turnstile"].required = True
    signup_form.fields["turnstile"].client_ip = client_ip

    if (
        registration_form.is_valid()
        and signup_form.is_valid()
        and farmer_form.is_valid()
    ):

        new_farmer = farmer_form.save(commit=False)
        new_registrant = registration_form.save(commit=False)
        new_user = signup_form.save(commit=False)

        new_farmer.user = new_user
        new_farmer.save()

        new_registrant.farmer = new_farmer
        new_registrant.survey_year = survey_year

        new_registrant.save()
        new_user.save()

        return redirect("registration_table")
    else:
        return render(
            request,
            "wisccc/wisc_cc_register_by_mgmt.html",
            {
                "registration_form": registration_form,
                "form_farmer": farmer_form,
                "form": signup_form,
            },
        )


@login_required
def wisc_cc_register_3(request):
    """Thank you for registering page"""

    return render(request, "wisccc/wisc_cc_register_3.html")


@permission_required("wisccc.survery_manager", raise_exception=True)
def upload_photo(request, id):
    """For uploading photos for survey response,
    from survey farm id"""
    context = {}
    # fetch the survey object related to passed id
    survey_farm = get_object_or_404(SurveyFarm, id=id)
    first_and_last_name = (
        f"{survey_farm.farmer.first_name} {survey_farm.farmer.last_name}"
    )
    survey_year = f"{survey_farm.survey_year}"
    survey_field = SurveyField.objects.filter(survey_farm_id=survey_farm.id).first()
    # Get any uploaded photos for this survey response
    survey_photo = SurveyPhoto.objects.filter(survey_field_id=survey_field.id).first()

    survey_photo_form = SurveyPhotoForm(request.POST or None, instance=survey_photo)
    # save the data from the form and
    # redirect to detail_view

    if survey_photo_form.is_valid():

        new_survey_photo = survey_photo_form.save()
        new_survey_photo.survey_field_id = survey_field.id
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
            "first_and_last_name": first_and_last_name,
            "survey_year": survey_year,
        },
    )


def wisc_cc_interested_agronomist(request):

    form_interested_agronomist = InterestedAgronomistForm(request.POST or None)
    # save the data from the form and
    # redirect to detail_view

    if form_interested_agronomist.is_valid():
        form_interested_agronomist.save()
        # new_form = form_interested_party.save(commit=False)
        # new_form.save()
        return redirect("wisc_cc_interested_agronomist_thanks")

    return render(
        request,
        "wisccc/wisc_cc_interested_agronomist.html",
        {"form_interested_agronomist": form_interested_agronomist},
    )


def wisc_cc_interested_agronomist_thanks(request):
    return render(request, "wisccc/wisc_cc_interested_agronomist_thanks.html")


@permission_required("wisccc.survery_manager", raise_exception=True)
def update_interested_agronomist(request, id):
    """For updating interested_agronomist"""
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the survey object related to passed id
    interested_agronomist = get_object_or_404(InterestedAgronomist, id=id)

    # pass the object as instance in form
    form_interested_agronomist = InterestedAgronomistForm(
        request.POST or None, instance=interested_agronomist
    )

    # save the data from the form and
    # redirect to detail_view

    if form_interested_agronomist.is_valid():

        form_interested_agronomist.save()

        return redirect("interested_agronomist_table")
    # add form dictionary to context
    context["form_interested_agronomist"] = form_interested_agronomist

    return render(request, "wisccc/wisc_cc_interested_agronomist_review.html", context)


@permission_required("wisccc.survery_manager", raise_exception=True)
def delete_interested_agronomist(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(InterestedAgronomist, id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("interested_agronomist_table")

    return render(request, "wisccc/delete_interested_agronomist.html", context)


@permission_required("wisccc.survery_manager", raise_exception=True)
def interested_agronomist_table(request):
    """List interested agronomists"""

    def get_table_data():
        """For getting interested agronomist data"""
        query = """
            select
                ia.id
                , ia.signup_timestamp::date as signup
                , ia.first_name
                , ia.last_name
                , ia.availability
                , ia.email
                , ia.admin_notes
            from wisccc_interestedagronomist ia"""
        dat = pd.read_sql(query, connection)
        dat = dat.to_dict("records")

        return dat

    data = get_table_data()

    table = InterestedAgronomistTable(data)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    return render(
        request,
        "wisccc/interested_agronomist_table.html",
        {"table": table},
    )
