from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
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
    success_url = reverse_lazy('kanopy_table')
    
class GroundcoverUpdateView(UpdateView):

    model = Groundcoverdoc    
    form_class = GroundcoverForm
    template_name = 'kanopy/kanopy_update_form.html'
    success_url = reverse_lazy('kanopy_table')

def kanopy_download(request):

    qs = Groundcoverdoc.objects.all()
    return djqscsv.render_to_csv_response(qs)

@login_required
@permission_required('kanopy.can_view_submissions', raise_exception=True)
def kanopy_table(request):
    """List Kanopy entries"""

    table = KanopyTable(Groundcoverdoc.objects.all())
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    return render(request, "kanopy/kanopy_table.html", {"table": table})

def kanopy_home(request):

    return render(request, 'kanopy/kanopy_home.html')
    
def kanopy_thanks(request):

    return render(request, 'kanopy/kanopy_thanks.html')
    
@permission_required('kanopy.can_view_submissions', raise_exception=True)
def kanopy_submission_map(request):
    docs = Groundcoverdoc.objects.all() 
    return render(request, 'kanopy/kanopy_submission_map.html', {'docs': docs})
    
def kanopy_submissions_json(request):
    
    # from django.db import connection

    def get_submissions_json():
        with connection.cursor() as cursor:
            cursor.execute("""
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
                  FROM (SELECT * FROM kanopy_groundcoverdoc) inputs) features;
            """)
            rows = cursor.fetchone()

        return rows
        
    data = get_submissions_json()
    # retrieve signed url for accessing private s3 images
    # There is probably a better way to do this but while there aren't many
    #   submissions this is fine.
    for feat in data[0]['features']:
        id = feat['id']
        
        submission_object = Groundcoverdoc.objects.get(pk = id)
        feat['properties']['image_url'] = submission_object.image.url
    
    
    return JsonResponse(list(data), safe=False)


def model_form_upload(request):
    if request.method == 'POST':
        form = GroundcoverForm(request.POST, request.FILES)
        if form.is_valid():
            new_point = form.save()
            # Submission object is a list of each uploaded point
            # If there is no submissions object then create it
            # else create it
            vals = {
                "pk":                    new_point.id,
                "location_name":  new_point.location_name,
                "uploaded_at":      new_point.uploaded_at.strftime("%c"),
                "image":               new_point.image.name,
                "image_url":          new_point.image.url
                }
                
            if request.session.get('submissions', False):
                # Refreshing the signed urls for previously uploaded images
                #   Best would be to see if the signed url had already expired, but unsure how to precisely do that.
                for sub in request.session['submissions']:
                    submission_object = Groundcoverdoc.objects.get(pk = sub['pk'])
                    sub['image_url'] = submission_object.image.url
                
                request.session['submissions'] += [ vals ]
                
            else:
                request.session['submissions'] = [ vals ]
            
            # Here do the county lookup
            # new_point.county = find_county()
            
            # Here pull long and lat from point field
            # new_point.long = new_point.collection_point.coords[0]
            # new_point.lat = new_point.collection_point.coords[1]
            
            return redirect('kanopy_thanks')
    else:
        form = GroundcoverForm()
        
    template = 'kanopy/model_form_upload.html'
    return render(request, template, {
            'form': form,
        })


class MapView(TemplateView):
    template_name = 'kanopy/geo_sample_template.html'

    def get_context(self, **kwargs):
        context = {'samplepoint': SamplepointForm()}
        return context


class DocSerializer(serializers.ModelSerializer):

    class Meta:
        model = Groundcoverdoc
        fields = '__all__'

def get_submission_freq():

    with connection.cursor() as cursor:
        cursor.execute("""
        with minmaxdate as (
            select Date(min(uploaded_at)) as dt_min_upload, Date(max(uploaded_at)) as dt_max_upload
            from kanopy_groundcoverdoc
        ), alldays as (
            select generate_series(dt_min_upload, dt_max_upload, interval '1 day')::date as dt_seq
            from minmaxdate
        ), upldfreq as (
            select Date(uploaded_at) dt_uploaded, count(*) as num_uploads
            from kanopy_groundcoverdoc
            group by dt_uploaded
            order by dt_uploaded
        ), rslt as (
            select
                dt_seq
                , num_uploads
            from alldays
            left join upldfreq
            on alldays.dt_seq = dt_uploaded
            order by dt_seq
            )
        select jsonb_build_object( 'dt_seq', dt_seq, 'num_uploads', num_uploads)
        from rslt       
        """)
        rows = cursor.fetchall()
    
    return rows

def kanopy_sub_graph(request):

    # query for frequence of uploades by date
    submission_freq = get_submission_freq()
    # Pulling just the first obj so not a list of 1 length tuples
    submission_freq = [i[0] for i in submission_freq]
    return render(request, 'kanopy/submission_barchart.html', 
        {'freq': json.dumps(submission_freq)})

@permission_required('kanopy.can_view_submissions', raise_exception=True)
def kanopy_submissions(request):

    # query for frequence of uploades by date
    submission_freq = get_submission_freq()
    # Pulling just the first obj so not a list of 1 length tuples
    submission_freq = [i[0] for i in submission_freq]

    # Get queryset
    docs = Groundcoverdoc.objects.all()
    # Groundcoverdoc.objects.annotate(date_uploaded = Cast('uploaded_at', DateField())).values("date_uploaded").annotate(total=Count("date_uploaded"))
    # Serialize entire queryset to Python native data type
    result = DocSerializer(docs, many=True)

    sjdocs = JSONRenderer().render(result.data)

    # Serialize into a json representation, which is a string
    #   Passing this to the template and using the 'safe' keyword
    #   allows the browser to see this as a JSON object, ex:
    # var sjdocs = {{ sjdocs|safe }};
    # sjdocs = serializers.serialize("json", docs)
    
    return render(request, 'kanopy/kanopy_submissions.html', 
        {'freq': json.dumps(submission_freq), "sjdocs": sjdocs.decode('UTF-8')})


def sample_point_form_upload(request):
    if request.method == 'POST':
        form = SamplepointForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kanopy_sample')
    else:
        form = SamplepointForm()
    return render(request, 'kanopy/geo_sample_template.html', {
        'form': form
    })
