# Kanopy -> Green CovR

Iframes can be used to pull in a map on a different website. 
To allow an external site to use a view from EvansGeospatial in an iframe then 
for that view one needs to 
```python
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def my_view_to_be_iframed():
   pass
```



## TODO

 - Async for growing degree days and county lookup
   - https://testdriven.io/blog/django-async-views/
   - https://stackoverflow.com/questions/76172946/access-to-model-attributes-and-methods-in-django-4-2-after-async-call-for-model
   - 
 - Tests for models and forms and etc
 - Separate form for cover crop types
   - https://stackoverflow.com/questions/4789466/populate-a-django-form-with-data-from-database-in-view
 - Validation
      - cover crop 1 should not allow nulls, but the rest should. Can I do this and still use all the same `choices` object?
 - Extract form to separate template
 - build in 'Logged in as' to footer    
 - Change App name
 - provide filtering for exporting data
 - Use modal to view images?
 - Add in toggle for satelite view, django leaflet?
 - Model work:
    - ** COMPLETED ** County lookup from point
    - split out lattitude and longitude from point field
 - Help text?
 - Verify that it is clear when errors occur
 - ** COMPLETED ** Rework names for better consistency
    - groundcoverdoc to greencover_submission
    - urls
 - ** COMPLETED ** https
 - ** COMPLETED ** Permissions:
    - use built in permissions
    - alter table view so 'update' and 'delete' only show based on permissions
 - ** COMPLETED ** Map view of submissions    
 - ** COMPLETED ** Figure out email capability for password reset
 - ** COMPLETED ** Show uploads from the current session
 - ** COMPLETED ** Export data function
 - ** COMPLETED ** Good vs Bad examples
 - ** COMPLETED ** Why is the label option for `collectionpoint` not showing up on the form? A: I forgot `|as_crispy_field`
 - ** COMPLETED ** Date picker
 - ** COMPLETED ** Integrate FGCC: https://github.com/fgcc-app/fgcc-app.github.io
 - ** COMPLETED ** Add necessary fields
 - ** COMPLETED ** Add email field, not required
 - ** COMPLETED ** Image browsing feature for Anna
 - ** COMPLETED ** Change from base.html so that it looks different from the rest of the site