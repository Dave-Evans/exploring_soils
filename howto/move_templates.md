# Reorganizing templates

I started this Django project thinking there would be only one or, at most, two apps.
At the beginning, I have put all the templates within the root template folder.
Now that there are five or more apps, it is not only difficult to find a particular template but I fear that I may want to have the same name for different templates across apps.

I am going to resolve this by following [this post)[stackoverflow.com/questions/15411164] on StackOverflow as well as [this article](docs.djangoproject.com/en/1.11/intro/tutorial03).

I have moved the template for bike mileage table, `mileage_template.html` from `root/templates/mileage_template.html` to `root/bikemileage/templates/bikemileage/mileage_template.html` and then added `bikemileage/` to the template name in the view.

When moving from root `templates` folder to a `app/templates/app` folder, all that needs to be changed is the reference to the `template_name.html` file by added `appname/template_name.html` to all references.

