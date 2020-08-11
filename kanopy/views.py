from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig
from kanopy.forms import GroundcoverForm
from kanopy.models import Groundcoverdoc
from kanopy.tables import (
    KanopyTable,
)


# @method_decorator(login_required, name='dispatch')
class GroundcoverDeleteView(DeleteView):

    model = Groundcoverdoc    
    success_url = reverse_lazy('kanopy_table')


def kanopy_table(request):
    """List Kanopy entries"""

    table = KanopyTable(Groundcoverdoc.objects.all())
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    return render(request, "kanopy/kanopy_table.html", {"table": table})

def kanopy_home(request):

    return render(request, 'kanopy/kanopy_home.html')
    
def kanopy_thanks(request):

    return render(request, 'kanopy/kanopy_thanks.html')
    

def model_form_upload(request):
    if request.method == 'POST':
        form = GroundcoverForm(request.POST, request.FILES)
        if form.is_valid():
            new_point = form.save()
            
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
