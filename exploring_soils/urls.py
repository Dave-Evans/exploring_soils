"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path
from django.contrib.auth import views as auth_views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from accounts import views as accounts_views
from boards import views
from plotter import views as plotter_views
from books import views as books_views
from bikemileage import views as mileage_views
from bikemileage.views import CustomMileageListView, MileageCreateView, MileageUpdateView, MileageDeleteView
from bikemileage.views import BicycleListView, BicycleCreateView, BicycleUpdateView, BicycleDeleteView
from kanopy import views as kanopy_views


urlpatterns = [
    

    re_path(r'^new_study/$', plotter_views.new_study, name='new_study'),
    re_path(r'^edit_study/(?P<pk>\d+)$', plotter_views.edit_study, name='edit_study'),
    re_path(r'^studies/$', plotter_views.studies, name='studies'),
    re_path(r'^explore_soils/$', plotter_views.soils_in_depth, name='explore_soils'),
    re_path(r'^soils_in_depth/$', plotter_views.soils_in_depth, name='soils_in_depth'),
    re_path(r'^pull_soils/(?P<minx>-?\d+\.\d+)/(?P<miny>-?\d+\.\d+)/(?P<maxx>-?\d+\.\d+)/(?P<maxy>-?\d+\.\d+)/$', plotter_views.pull_soils, name='pull_soils'),
    re_path(r'^studies/(?P<pk>\d+)/add_rep/$', plotter_views.add_rep, name='add_rep'),
    re_path(r'^studies/(?P<pk>\d+)/retrieve_existing_reps/$', plotter_views.retrieve_existing_reps, name='retrieve_existing_reps'),

    re_path(r'^studies/get_rep/(?P<pk>\d+)/(?P<lly>-?\d+\.\d+)/(?P<llx>-?\d+\.\d+)/(?P<uly>-?\d+\.\d+)/(?P<ulx>-?\d+\.\d+)/$', plotter_views.get_plots, name='get_plots'),
    # bikemileage App
    # re_path(r'^mileage/$',mileage_views.mileage_list, name='mileage_list' ),
    path('custom_mileage', CustomMileageListView.as_view() , name='custom_mileage' ),
    re_path(r'^mileage/create/$', MileageCreateView.as_view(), name='mileage_create'),
    re_path(r'^mileage/delete/(?P<pk>\d+)/', MileageDeleteView.as_view(), name='mileage_delete'),
    path('mileage/<int:pk>/edit/', MileageUpdateView.as_view(), name='mileage_update'),

    path('bicycles', BicycleListView.as_view(), name='bicycle_list'),
    path('bicycles/create', BicycleCreateView.as_view(), name='bicycle_create'),
    path('bicycles/<int:pk>/', BicycleUpdateView.as_view(), name='bicycle_update'),
    path('bicycles/<int:pk>/delete', BicycleDeleteView.as_view(), name='bicycle_delete'),

    re_path(r'^signup/$', accounts_views.signup, name='signup'),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    
    # Kanopy app
    re_path(r'^kanopy$', kanopy_views.kanopy_home, name='kanopy_home'),
    re_path(r'^kanopy/delete/(?P<pk>\d+)/', kanopy_views.GroundcoverDeleteView.as_view(), name='groundcover_delete'),
    path('groundcover_update/<int:pk>/', kanopy_views.GroundcoverUpdateView.as_view(), name='groundcover_update'),
    re_path(r'^kanopy_thanks$', kanopy_views.kanopy_thanks, name='kanopy_thanks'),
    re_path(r'^kanopy_map$', kanopy_views.kanopy_submission_map, name='kanopy_submission_map'),
    re_path(r'^kanopy_submissions_json$', kanopy_views.kanopy_submissions_json, name='kanopy_submissions_json'),
    re_path(r'^kanopy_table$', kanopy_views.kanopy_table, name='kanopy_table'),
    re_path(r'^kanopy_upload$', kanopy_views.model_form_upload, name='kanopy_upload'),
    re_path(r'^kanopy_download$', kanopy_views.kanopy_download, name='kanopy_download'),
    re_path(r'^kanopy/datalook/20201230$', kanopy_views.datalook_20201230, name='datalook_20201230'),
    # re_path(r'^kanopy_sample$', kanopy_views.sample_point_form_upload, name='kanopy_sample'),
    # re_path(r'^kanopy_sample$', kanopy_views.addPointOnMap, name='kanopy_sample'),
    # re_path(r'^kanopy_sample$', kanopy_views.MapView.as_view(), name='kanopy_sample'),
    
    

    # Books app
    re_path(r'^$', books_views.home, name="home"),
    re_path(r'^books/$', books_views.book_list, name="book_list"),
    re_path(r'^books/create/$', books_views.book_create, name='book_create'),
    re_path(r'^books/(?P<pk>\d+)/update/$', books_views.book_update, name='book_update'),
    re_path(r'^books/(?P<pk>\d+)/delete/$', books_views.book_delete, name='book_delete'),
    
    # Accounts
    re_path(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    re_path(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),

    re_path(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    re_path(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    re_path(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    re_path(r'^settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account'),
        
    # Boards 
    re_path(r'^boards$', views.BoardListView.as_view(), name='home_boards'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post'),
    re_path(r'^new_post/$', views.NewPostView.as_view(), name='new_post'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),
    # re_path(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    re_path(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
    re_path(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
