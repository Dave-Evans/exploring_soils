from django.shortcuts import render, redirect, get_object_or_404

from kanopy.forms import GroundcoverForm

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
