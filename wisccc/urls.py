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
        r"^wisc_cc_register$",
        wisccc_views.wisc_cc_register_1,
        name="wisc_cc_register_1",
    ),
    re_path(
        r"^wisc_cc_register_1$",
        wisccc_views.wisc_cc_register_1,
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
    # For creating an account
    re_path(
        r"^wisc_cc_signup$",
        wisccc_views.wisc_cc_signup,
        name="wisc_cc_signup",
    ),
    # For Logging in when one already has an account
    re_path(
        r"login/",
        auth_views.LoginView.as_view(
            template_name="wisccc/wisc_cc_login.html", authentication_form=UserLoginForm
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
    # path("create_photo/<id>", wisccc_views.update_response, name="create_photo"),
    # path("update_photo/<id>", wisccc_views.update_response, name="update_photo"),
    # re_path(
    #     r"^wisccc_download_data/<int:opt>$",
    #     wisccc_views.wisccc_download_data,
    #     name="wisccc_download_data",
    # ),
    path(
        "wisccc_download_data/<int:opt>",
        wisccc_views.wisccc_download_data,
        name="wisccc_download_data",
    ),
    # Temporarily directing people to the home page rather than the survey page.
    re_path(r"^wisc-cc-survey$", wisccc_views.wisc_cc_home, name="wisc_cc_survey"),
    # re_path(r"^wisc-cc-survey$", wisccc_views.wisc_cc_survey, name="wisc_cc_survey"),
    re_path(
        r"^wisc-cc-survey/0$", wisccc_views.wisc_cc_survey0, name="wisc_cc_survey0"
    ),
    re_path(
        r"^wisc-cc-survey/1$", wisccc_views.wisc_cc_survey1, name="wisc_cc_survey1"
    ),
    re_path(
        r"^wisc-cc-survey/2$", wisccc_views.wisc_cc_survey2, name="wisc_cc_survey2"
    ),
    re_path(
        r"^wisc-cc-survey/3$", wisccc_views.wisc_cc_survey3, name="wisc_cc_survey3"
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
