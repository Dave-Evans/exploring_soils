from django.urls import re_path, path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from wisccc import views as wisccc_views
from wisccc.forms import UserLoginForm

urlpatterns = [
    re_path(r"^wisc-cc-home$", wisccc_views.wisc_cc_home, name="wisc_cc_home"),
    re_path(r"^wisc_cc_home$", wisccc_views.wisc_cc_home, name="wisc_cc_home"),
    re_path(
        r"^wisc_cc_manager_home$",
        wisccc_views.wisc_cc_manager_home,
        name="wisc_cc_manager_home",
    ),
    re_path(
        r"^wisc_cc_manager$",
        wisccc_views.wisc_cc_manager_home,
        name="wisc_cc_manager_home",
    ),
    re_path(
        r"^wisc_cc_about$",
        wisccc_views.wisc_cc_about,
        name="wisc_cc_about",
    ),
    re_path(
        r"^wisc_cc_admin$",
        wisccc_views.wisc_cc_manager_home,
        name="wisc_cc_manager_home",
    ),
    re_path(
        r"^wisc_cc_interested$",
        wisccc_views.wisc_cc_interested,
        name="wisc_cc_interested",
    ),
    re_path(
        r"^wisc_cc_interested_table$",
        wisccc_views.interested_party_table,
        name="interested_party_table",
    ),
    path(
        "update_interested_party/<id>",
        wisccc_views.update_interested_party,
        name="update_interested_party",
    ),
    path(
        "delete_interested_party/<id>",
        wisccc_views.delete_interested_party,
        name="delete_interested_party",
    ),
    re_path(
        r"^wisc_cc_interested_thanks$",
        wisccc_views.wisc_cc_interested_thanks,
        name="wisc_cc_interested_thanks",
    ),
    re_path(
        r"^wisc_cc_interested_agronomist$",
        wisccc_views.wisc_cc_interested_agronomist,
        name="wisc_cc_interested_agronomist",
    ),
    re_path(
        r"^wisc_cc_interested_agronomist_table$",
        wisccc_views.interested_agronomist_table,
        name="interested_agronomist_table",
    ),
    path(
        "update_interested_agronomisty/<id>",
        wisccc_views.update_interested_agronomist,
        name="update_interested_agronomist",
    ),
    path(
        "delete_interested_agronomist/<id>",
        wisccc_views.delete_interested_agronomist,
        name="delete_interested_agronomist",
    ),
    re_path(
        r"^wisc_cc_interested_agronomist_thanks$",
        wisccc_views.wisc_cc_interested_agronomist_thanks,
        name="wisc_cc_interested_agronomist_thanks",
    ),
    re_path(
        r"^wisc_cc_register_1$",
        wisccc_views.wisc_cc_interested,
        name="wiscc_cc_interested",
        # wisccc_views.wisc_cc_register_1,
        # name="wisc_cc_register_1",
    ),
    re_path(
        r"^wisc_cc_register_1$",
        wisccc_views.wisc_cc_interested,
        # wisccc_views.wisc_cc_register_1,
        name="wisc_cc_register_1",
    ),
    re_path(
        r"^wisc_cc_register_2$",
        wisccc_views.wisc_cc_register_2,
        name="wisc_cc_register_2",
    ),
    re_path(
        r"^wisc_cc_register_3$",
        wisccc_views.wisc_cc_register_3,
        name="wisc_cc_register_3",
    ),
    re_path(
        r"^wisc_cc_register_by_mgmt$",
        wisccc_views.wisc_cc_register_by_mgmt,
        name="wisc_cc_register_by_mgmt",
    ),
    re_path(
        r"^wisc_cc_register_by_mgmt_exist_user_select$",
        wisccc_views.wisc_cc_register_by_mgmt_exist_user_select,
        name="wisc_cc_register_by_mgmt_exist_user_select",
    ),
    # Takes the user's pk
    path(
        "wisc_cc_register_by_mgmt_exist_user/<pk>",
        wisccc_views.wisc_cc_register_by_mgmt_exist_user,
        name="wisc_cc_register_by_mgmt_exist_user",
    ),
    # For creating an account
    re_path(r"^signup/$", wisccc_views.wisc_cc_signup, name="signup"),
    re_path(
        r"^wisc_cc_signup$",
        wisccc_views.wisc_cc_signup,
        name="wisc_cc_signup",
    ),
    # For Logging in when one already has an account
    re_path(
        r"login/",
        auth_views.LoginView.as_view(
            template_name="wisccc/wisc_cc_login.html",
            authentication_form=UserLoginForm,
            next_page="wisc_cc_home",
        ),
        name="login",
    ),
    re_path(
        r"register_1a/",
        auth_views.LoginView.as_view(
            template_name="wisccc/wisc_cc_register_1_login.html",
            authentication_form=UserLoginForm,
        ),
        name="register_1a",
    ),
    path("upload_photo/<id>", wisccc_views.upload_photo, name="upload_photo"),
    path("update_response/<id>", wisccc_views.update_response, name="update_response"),
    path("delete_response/<id>", wisccc_views.delete_response, name="delete_response"),
    path("update_labdata/<id>", wisccc_views.update_labdata, name="update_labdata"),
    re_path(r"^response_table$", wisccc_views.response_table, name="response_table"),
    re_path(
        r"^registration_table$",
        wisccc_views.registration_table,
        name="registration_table",
    ),
    path(
        "update_registration/<id>",
        wisccc_views.update_registration,
        name="update_registration",
    ),
    path(
        "delete_registration/<id>",
        wisccc_views.delete_registration,
        name="delete_registration",
    ),
    path(
        "download_registrants",
        wisccc_views.download_registrants,
        name="download_registrants",
    ),
    # path("create_photo/<id>", wisccc_views.update_response, name="create_photo"),
    # path("update_photo/<id>", wisccc_views.update_response, name="update_photo"),
    # re_path(
    #     r"^wisccc_download_data/<int:opt>$",
    #     wisccc_views.wisccc_download_data,
    #     name="wisccc_download_data",
    # ),
    re_path(
        r"^researcher_table$", wisccc_views.researcher_table, name="researcher_table"
    ),
    path(
        "update_researcher/<id>",
        wisccc_views.update_researcher,
        name="update_researcher",
    ),
    path(
        "delete_researcher/<id>",
        wisccc_views.delete_researcher,
        name="delete_researcher",
    ),
    path(
        "download_researchers",
        wisccc_views.download_researchers,
        name="download_researchers",
    ),
    path(
        "wisccc_download_data/<int:opt>",
        wisccc_views.wisccc_download_data,
        name="wisccc_download_data",
    ),
    re_path(
        r"^wisccc-create-researcher$",
        wisccc_views.wisccc_create_researcher,
        name="wisccc_create_researcher",
    ),
    re_path(
        r"^wisccc-create-researcher-existing-user$",
        wisccc_views.wisccc_create_researcher_existing_user,
        name="wisccc_create_researcher_existing_user",
    ),
    re_path(r"^researcher_page$", wisccc_views.researcher_page, name="researcher_page"),
    re_path(
        r"^researcher_page_unapproved$",
        wisccc_views.researcher_page_unapproved,
        name="researcher_page_unapproved",
    ),
    re_path(
        r"^researcher_page_expired$",
        wisccc_views.researcher_page_expired,
        name="researcher_page_expired",
    ),
    re_path(
        r"^wisccc_researcher_download_data$",
        wisccc_views.wisccc_researcher_download_data,
        name="wisccc_researcher_download_data",
    ),
    # Temporarily directing people to the home page rather than the survey page.
    re_path(r"^wisc-cc-survey$", wisccc_views.wisc_cc_survey, name="wisc_cc_survey"),
    re_path(
        r"^wisc-cc-survey/1$", wisccc_views.wisc_cc_survey1, name="wisc_cc_survey1"
    ),
    re_path(
        r"^wisc-cc-survey/2$", wisccc_views.wisc_cc_survey2, name="wisc_cc_survey2"
    ),
    re_path(
        r"^wisc-cc-survey/3a$", wisccc_views.wisc_cc_survey3a, name="wisc_cc_survey3a"
    ),
    re_path(
        r"^wisc-cc-survey/3$", wisccc_views.wisc_cc_survey3, name="wisc_cc_survey3"
    ),
    re_path(
        r"^wisc-cc-survey/4$", wisccc_views.wisc_cc_survey4, name="wisc_cc_survey4"
    ),
    re_path(
        r"^wisc-cc-survey/5$", wisccc_views.wisc_cc_survey5, name="wisc_cc_survey5"
    ),
    re_path(
        r"^wisc-cc-survey/6$", wisccc_views.wisc_cc_survey6, name="wisc_cc_survey6"
    ),
    re_path(
        r"^wisc-cc-survey/7$", wisccc_views.wisc_cc_survey7, name="wisc_cc_survey7"
    ),
    path(
        "update_fieldfarm/<id>",
        wisccc_views.update_fieldfarm,
        name="update_fieldfarm",
    ),
    path(
        "create_fieldfarm",
        wisccc_views.create_fieldfarm,
        name="create_fieldfarm",
    ),
    path(
        "wisc_cc_survey_populate_fieldfarm/<id>",
        wisccc_views.wisc_cc_survey_populate_fieldfarm,
        name="wisc_cc_survey_populate_fieldfarm",
    ),
    re_path(r"^wisc-cc-graph$", wisccc_views.wisc_cc_graph, name="wisc_cc_graph"),
    re_path(r"^wisc_cc_graph$", wisccc_views.wisc_cc_graph, name="wisc_cc_graph"),
    re_path(r"^wisc-cc-map$", wisccc_views.wisc_cc_map, name="wisc_cc_map"),
    re_path(r"^wisc_cc_map$", wisccc_views.wisc_cc_map, name="wisc_cc_map"),
    re_path(r"^wisc_cc_map$", wisccc_views.wisc_cc_map, name="wisc_cc_map"),
    re_path(
        r"^wisc-cc-map-embed$", wisccc_views.wisc_cc_map_embed, name="wisc_cc_map_embed"
    ),
    re_path(
        r"^wisc_cc_map_embed$", wisccc_views.wisc_cc_map_embed, name="wisc_cc_map_embed"
    ),
    re_path(
        r"^wisc_cc_static_data$",
        wisccc_views.wisc_cc_static_data,
        name="wisc_cc_static_data",
    ),
    re_path(
        r"^get_wisc_cc_data$",
        wisccc_views.get_wisc_cc_data,
        name="get_wisc_cc_data",
    ),
    re_path(
        r"^get_wi_counties$",
        wisccc_views.get_wi_counties,
        name="get_wi_counties",
    ),
]
