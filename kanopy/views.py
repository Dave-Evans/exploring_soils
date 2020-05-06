from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from kanopy.forms import GroundcoverForm, AddPointForm
from kanopy.models import Samplepoint

def model_form_upload(request):
    if request.method == 'POST':
        form = GroundcoverForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('kanopy_upload')
    else:
        form = GroundcoverForm()
    return render(request, 'kanopy/model_form_upload.html', {
        'form': form
    })


        
def addPointOnMap(request):
    if request.method == "POST":
        geoform = AddPointForm(request.POST or None)
        if geoform.is_valid():
            new_point = geoform.save()
            new_point.save()
            return redirect('kanopy_sample')
    else:
        geoform = AddPointForm()
        context = {
            'geoform': geoform,
        }
    template = 'kanopy/geo_sample_template.html'
    return render(request, template, context)
    

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
