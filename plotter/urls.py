from django.urls import re_path
from plotter import views as plotter_views

urlpatterns = [
    re_path(r"^new_study/$", plotter_views.new_study, name="new_study"),
    re_path(r"^edit_study/(?P<pk>\d+)$", plotter_views.edit_study, name="edit_study"),
    re_path(r"^studies/$", plotter_views.studies, name="studies"),
    re_path(r"^explore_soils/$", plotter_views.soils_in_depth, name="explore_soils"),
    re_path(r"^soils_in_depth/$", plotter_views.soils_in_depth, name="soils_in_depth"),
    re_path(
        r"^pull_soils/(?P<minx>-?\d+\.\d+)/(?P<miny>-?\d+\.\d+)/(?P<maxx>-?\d+\.\d+)/(?P<maxy>-?\d+\.\d+)/$",
        plotter_views.pull_soils,
        name="pull_soils",
    ),
    re_path(r"^studies/(?P<pk>\d+)/add_rep/$", plotter_views.add_rep, name="add_rep"),
    re_path(
        r"^studies/(?P<pk>\d+)/retrieve_existing_reps/$",
        plotter_views.retrieve_existing_reps,
        name="retrieve_existing_reps",
    ),
    re_path(
        r"^studies/get_rep/(?P<pk>\d+)/(?P<lly>-?\d+\.\d+)/(?P<llx>-?\d+\.\d+)/(?P<uly>-?\d+\.\d+)/(?P<ulx>-?\d+\.\d+)/$",
        plotter_views.get_plots,
        name="get_plots",
    ),
]