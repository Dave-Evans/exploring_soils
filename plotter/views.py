#https://www.techinfected.net/2016/08/how-to-change-your-django-project-name.html
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .forms import NewStudyForm, NewRepForm
from .models import Study, Rep
from .build_rep import *
from .pull_soils import *

# in order to make new topic, we need to pass
#   the information for which board it will belong
@login_required
def new_study(request):
    #board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()  # TODO: get the currently logged in user


    if request.method == 'POST':
        form = NewStudyForm(request.POST)
        if form.is_valid():
            study = form.save(commit=False)
            study.owner = request.user
            study.save()
            return redirect('studies')  # TODO: redirect to the created topic page
    else:
        form = NewStudyForm()
    return render(request, 'new_study.html', {'form': form})

def edit_study(request, pk):
    #board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()  # TODO: get the currently logged in user

    study = get_object_or_404(Study, pk=pk)
    if request.method == 'POST':
        form = NewStudyForm(request.POST, instance=study)
        if form.is_valid():
            study = form.save(commit=False)
            study.owner = request.user
            study.save()
            return redirect('studies')  # TODO: redirect to the created topic page
    else:
        form = NewStudyForm(instance=study)


    return render(request, 'new_study.html', {'form': form})



def studies(request):
    studies = Study.objects.all()
    return render(request, 'studies_home.html', {'studies': studies})

def explore_soils(request):

    return render(request, 'explore_soils.html')

def pull_soils(request, miny, minx, maxy, maxx):
    '''For downloading and processing soils data
    Note the actual function call has X,Y, while the view is lat, long'''
    bbox = {
        "minx" : minx,
        "miny" : miny,
        "maxx" : maxx,
        "maxy" : maxy
    }
    # json_soils = return_soils_json(llx, lly, urx, ury)
    json_soils = return_soils_json(bbox)
    return JsonResponse(json_soils, safe=True)

def add_rep(request, pk):
    '''Also add existing reps here. This will facilitate the expansion of this view
    from just adding to edit and deletion as well as facilitate the veiwing of existing reps
    https://gis.stackexchange.com/questions/252958/how-to-save-geodjango-forms
    '''
    study = get_object_or_404(Study, pk=pk)

    if request.method == 'POST':
        form = NewRepForm(request.POST)
        if form.is_valid():
            rep = form.save(commit=False)

            rep.study = study

            rep.save()
            return redirect('add_rep', pk)  # TODO: redirect to the created topic page
    else:
        form = NewRepForm()
        form.study = study

    return render(request, 'add_rep.html', {'study': study, 'form': form})


def get_plots(request, pk, lly, llx, uly, ulx):
    '''For returning a rep of plots
    pk is study pk.

    Here using query strings to grab ll and ul coords
    ?ll_x=2&ll_y=2&ul_x=2&ul_y=2
    for reference: https://stackoverflow.com/questions/3711349/django-and-query-string-parameters
    or https://stackoverflow.com/questions/2778247/how-do-i-construct-a-django-reverse-url-using-query-args
    '''
    study = get_object_or_404(Study, pk=pk)

    msg = '''
    Working on study {nm}
    with
        lower left y: {lly}
        lower left x: {llx}

        upper left y: {uly}
        upper left x: {ulx}
    '''.format(nm=study.name,
        lly=lly, llx=llx, uly=uly, ulx=ulx)
    print(msg)


    ulx = float(ulx)
    uly = float(uly)
    llx = float(llx)
    lly = float(lly)
    ## send to function
    ##  get back geoJSON
    json_plots = create_json_of_rep(lly, llx, uly, ulx, study)

    return JsonResponse(json_plots)




def retrieve_existing_reps(request, pk):

    study = get_object_or_404(Study, pk=pk)
    print("Getting all reps for Study {}".format(study.name))

    reps = study.reps.all()

    dict_polys = {
         "type": "FeatureCollection",
        "features": [
        ]
    }

    for rep in reps:
        json_plots = create_json_of_rep(
            rep.lower_left_corner_y,
            rep.lower_left_corner_x,
            rep.upper_left_corner_y,
            rep.lower_left_corner_x,
            study
        )
        dict_polys['features'] = dict_polys['features'] +\
            json_plots['features']


    return JsonResponse(json_plots)

    # json.dump(dict_polys, open("test_return.geojson", 'w'), indent=2)
