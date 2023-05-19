from django.urls import re_path, path
from django.views.generic import RedirectView
from kanopy import views as kanopy_views

urlpatterns = [
    re_path(r"^green_covr$", kanopy_views.kanopy_home, name="kanopy_home"),
    re_path(
        r"^kanopy/$",
        RedirectView.as_view(pattern_name="kanopy_home", permanent=False),
    ),
    re_path(
        r"^green_covr_references$",
        kanopy_views.green_covr_references,
        name="green_covr_references",
    ),
    re_path(
        r"^kanopy/delete/(?P<pk>\d+)/",
        kanopy_views.GroundcoverDeleteView.as_view(),
        name="groundcover_delete",
    ),
    path(
        "groundcover_update/<int:pk>/",
        kanopy_views.GroundcoverUpdateView.as_view(),
        name="groundcover_update",
    ),
    re_path(r"^green_covr_thanks$", kanopy_views.kanopy_thanks, name="kanopy_thanks"),
    re_path(
        r"^kanopy_thanks/$",
        RedirectView.as_view(pattern_name="kanopy_thanks", permanent=True),
    ),
    re_path(
        r"^green_covr_graph$",
        kanopy_views.kanopy_graph,
        name="green_covr_graph",
    ),
    re_path(
        r"^green_covr_map$",
        kanopy_views.kanopy_display_map,
        name="green_covr_submission_map",
    ),
    re_path(
        r"^kanopy_map/$",
        RedirectView.as_view(pattern_name="green_covr_submission_map", permanent=False),
    ),
    re_path(
        r"^kanopy_submissions_json$",
        kanopy_views.kanopy_submissions_json,
        name="kanopy_submissions_json",
    ),
    re_path(
        r"^county_map$",
        kanopy_views.county_map,
        name="county_map",
    ),
    re_path(
        r"^get_mn_counties$",
        kanopy_views.get_mn_counties,
        name="get_mn_counties",
    ),
    re_path(r"^green_covr_table$", kanopy_views.kanopy_table, name="kanopy_table"),
    re_path(
        r"^kanopy_table/$",
        RedirectView.as_view(pattern_name="kanopy_table", permanent=False),
    ),
    re_path(
        r"^green_covr_upload$", kanopy_views.model_form_upload, name="kanopy_upload"
    ),
    re_path(
        r"^kanopy_upload/$",
        RedirectView.as_view(pattern_name="kanopy_upload", permanent=False),
    ),
    re_path(
        r"^green_covr_download$", kanopy_views.kanopy_download, name="kanopy_download"
    ),
    re_path(
        r"^kanopy_download/$",
        RedirectView.as_view(pattern_name="kanopy_download", permanent=False),
    ),
    re_path(
        r"^green_covr/datalook/20201230$",
        kanopy_views.datalook_20201230,
        name="datalook_20201230",
    ),
    re_path(
        r"^kanopy/datalook/20201230/$",
        RedirectView.as_view(pattern_name="datalook_20201230", permanent=False),
    ),
    re_path(
        r"^green_covr/datalook/2020_21$",
        kanopy_views.datalook_2020_21,
        name="datalook_2020_21",
    ),
    re_path(
        r"^kanopy/datalook/2020_21/$",
        RedirectView.as_view(pattern_name="datalook_2020_21", permanent=False),
    ),
]