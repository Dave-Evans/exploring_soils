# Kanopy -> Green CovR

## TODO

 - Export data function
    - For now, raw dump, but should provide filtering in the future
 - Extract form to separate template
 - build in 'Logged in as' to footer    
 - Map view of submissions    
 - Figure out email capability for password reset
 - Change App name
 - Rework names for better consistency
        - groundcoverdoc to greencover_submission
        - urls
 
 - Use modal to view images?
 - Model work:
    - County lookup from point
    - split out lattitude and longitude from point field
 - https
 - Help text?
 - Verify that it is clear when errors occur
 - cover crop 1 should not allow nulls, but the rest should. Can I do this and still use all the same `choices` object?
 - Permissions:
    - use built in permissions
    - alter table view so 'update' and 'delete' only show based on permissions

 - ** COMPLETED ** Good vs Bad examples
 - ** COMPLETED ** Why is the label option for `collectionpoint` not showing up on the form? A: I forgot `|as_crispy_field`
 - ** COMPLETED ** Date picker
 - ** COMPLETED ** Integrate FGCC: https://github.com/fgcc-app/fgcc-app.github.io
 - ** COMPLETED ** Add necessary fields
 - ** COMPLETED **Add email field, not required
 - ** COMPLETED ** Image browsing feature for Anna
 - ** COMPLETED ** Change from base.html so that it looks different from the rest of the site