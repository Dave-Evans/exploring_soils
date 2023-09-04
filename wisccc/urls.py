from django.urls import re_path, path
from django.views.generic import RedirectView
from wisccc import views as wisccc_views

urlpatterns = [
    re_path(r"^wisc-cc-home$", wisccc_views.wisc_cc_home, name="wisc_cc_home"),
    re_path(r"^wisc_cc_home$", wisccc_views.wisc_cc_home, name="wisc_cc_home"),
    re_path(r"^wisc-cc-survey$", wisccc_views.wisc_cc_survey, name="wisc_cc_survey"),
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
        r"^get_wi_counties$",
        wisccc_views.get_wi_counties,
        name="get_wi_counties",
    ),
]
