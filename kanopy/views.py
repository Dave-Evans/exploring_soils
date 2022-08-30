from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.db import connection
from django_tables2 import RequestConfig
import djqscsv
import json
from kanopy.forms import GroundcoverForm
from kanopy.models import Groundcoverdoc
from kanopy.tables import (
    KanopyTable,
)


# @method_decorator(login_required, name='dispatch')
# class GroundcoverDeleteView(PermissionRequiredMixin, DeleteView):
class GroundcoverDeleteView(DeleteView):

    model = Groundcoverdoc
    success_url = reverse_lazy("kanopy_table")


class GroundcoverUpdateView(UpdateView):

    model = Groundcoverdoc
    form_class = GroundcoverForm
    template_name = "kanopy/kanopy_update_form.html"
    success_url = reverse_lazy("kanopy_table")


@permission_required("kanopy.can_view_submissions", raise_exception=True)
def kanopy_download(request):

    qs = Groundcoverdoc.objects.all()
    return djqscsv.render_to_csv_response(qs)


@login_required
@permission_required("kanopy.can_view_submissions", raise_exception=True)
def kanopy_table(request):
    """List Kanopy entries"""

    table = KanopyTable(Groundcoverdoc.objects.all())
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    return render(request, "kanopy/kanopy_table.html", {"table": table})


def kanopy_home(request):

    return render(request, "kanopy/kanopy_home.html")


def kanopy_thanks(request):

    return render(request, "kanopy/kanopy_thanks.html")


def green_covr_references(request):

    return render(request, "kanopy/kanopy_references.html")


@permission_required("kanopy.can_view_submissions", raise_exception=True)
def kanopy_graph(request):
    docs = Groundcoverdoc.objects.all()
    return render(request, "kanopy/kanopy_graph.html", {"docs": docs})


@permission_required("kanopy.can_view_submissions", raise_exception=True)
def kanopy_submission_map(request):
    docs = Groundcoverdoc.objects.all()
    return render(request, "kanopy/kanopy_submission_map.html", {"docs": docs})


@permission_required("kanopy.can_view_submissions", raise_exception=True)
def kanopy_display_map(request):
    docs = Groundcoverdoc.objects.all()
    return render(request, "kanopy/kanopy_display_map.html", {"docs": docs})


@permission_required("kanopy.can_view_submissions", raise_exception=True)
def kanopy_submissions_json(request):

    # from django.db import connection

    def get_submissions_json():
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
                        , geom.photo_taken_date
                        , geom.image
                        , geom.uploaded_at
                        , geom.fgcc_value
                        , geom.cover_crop_species_1 
                        , geom.cover_crop_species_2
                        , geom.cover_crop_species_3 
                        , geom.cover_crop_species_4
                        , geom.cover_crop_planting_date 
                        , geom.cover_crop_termination_date 
                        , geom.cover_crop_planting_rate 
                        , geom.crop_prior 
                        , geom.crop_posterior 
                        , geom.cover_crop_interseeded 
                        , geom.gdd
                        , geom.county_name
                        , ST_GeometryN(ST_GeneratePoints(geom.b_collectionpoint, 1), 1) as collectionpoint 
                    FROM (
                        select 
                            *, ST_Buffer(collectionpoint, 0.02) as b_collectionpoint
                            from kanopy_groundcoverdoc
                        ) AS geom
                    ) as inputs) features;
            """
            )
            rows = cursor.fetchone()
            data = json.loads(rows[0])
        return data

    data = get_submissions_json()
    # retrieve signed url for accessing private s3 images
    # There is probably a better way to do this but while there aren't many
    #   submissions this is fine.
    for feat in data["features"]:
        id = feat["id"]

        submission_object = Groundcoverdoc.objects.get(pk=id)
        feat["properties"]["image_url"] = submission_object.image.url

    return JsonResponse(list(data["features"]), safe=False)


def county_map(request):

    return render(request, "kanopy/county_map.html")


def get_mn_counties(request):

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
                            -- , simple_shape as geom
                            -- , ST_Simplify(shape, 0.001) as geom
                            , shape as geom
                            from mn_counties
                    ) as inputs
                ) features;
            """
            )
            rows = cursor.fetchone()
            data = json.loads(rows[0])
        return data

    data = get_county_json()
    # retrieve signed url for accessing private s3 images
    # There is probably a better way to do this but while there aren't many
    #   submissions this is fine.
    # for feat in data["features"]:
    #     id = feat["id"]

    #     submission_object = Groundcoverdoc.objects.get(pk=id)
    #     feat["properties"]["image_url"] = submission_object.image.url

    # return JsonResponse(list(data["features"]), safe=False)

    return JsonResponse(data, safe=False)


def model_form_upload(request):
    if request.method == "POST":
        form = GroundcoverForm(request.POST, request.FILES)
        if form.is_valid():
            new_point = form.save()
            new_point.populate_gdd()
            new_point.populate_county()
            new_point.save()
            # Submission object is a list of each uploaded point
            # If there is no submissions object then create it
            # else create it
            vals = {
                "pk": new_point.id,
                "location_name": new_point.location_name,
                "uploaded_at": new_point.uploaded_at.strftime("%c"),
                "image": new_point.image.name,
                "image_url": new_point.image.url,
            }

            if request.session.get("submissions", False):
                # Refreshing the signed urls for previously uploaded images
                #   Best would be to see if the signed url had already expired, but unsure how to precisely do that.
                for sub in request.session["submissions"]:
                    submission_object = Groundcoverdoc.objects.get(pk=sub["pk"])
                    sub["image_url"] = submission_object.image.url

                request.session["submissions"] += [vals]

            else:
                request.session["submissions"] = [vals]

            # Here do the county lookup
            # new_point.county = find_county()

            # Here pull long and lat from point field
            # new_point.long = new_point.collection_point.coords[0]
            # new_point.lat = new_point.collection_point.coords[1]

            return redirect("kanopy_thanks")
    else:
        form = GroundcoverForm()

    template = "kanopy/model_form_upload.html"
    return render(
        request,
        template,
        {
            "form": form,
        },
    )


def datalook_20201230(request):

    return render(request, "kanopy/green_covr_data_look_20201230.html")


def datalook_2020_21(request):

    return render(request, "kanopy/green_covr_data_look_2020_21.html")


def kanopy_redirect(request):
    """For redirecting to Green Covr urls"""
    response = redirect("/green_covr")
    return response
