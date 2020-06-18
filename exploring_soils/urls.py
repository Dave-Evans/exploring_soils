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
from django.conf.urls import url
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
    url(r'^$', views.BoardListView.as_view(), name='home'),
    url(r'^new_study/$', plotter_views.new_study, name='new_study'),
    url(r'^edit_study/(?P<pk>\d+)$', plotter_views.edit_study, name='edit_study'),
    url(r'^studies/$', plotter_views.studies, name='studies'),
    url(r'^explore_soils/$', plotter_views.explore_soils, name='explore_soils'),
    url(r'^pull_soils/(?P<lly>-?\d+\.\d+)/(?P<llx>-?\d+\.\d+)/(?P<ury>-?\d+\.\d+)/(?P<urx>-?\d+\.\d+)/$', plotter_views.pull_soils, name='pull_soils'),
    url(r'^studies/(?P<pk>\d+)/add_rep/$', plotter_views.add_rep, name='add_rep'),
    url(r'^studies/(?P<pk>\d+)/retrieve_existing_reps/$', plotter_views.retrieve_existing_reps, name='retrieve_existing_reps'),

    url(r'^studies/get_rep/(?P<pk>\d+)/(?P<lly>-?\d+\.\d+)/(?P<llx>-?\d+\.\d+)/(?P<uly>-?\d+\.\d+)/(?P<ulx>-?\d+\.\d+)/$', plotter_views.get_plots, name='get_plots'),
    # bikemileage App
    # url(r'^mileage/$',mileage_views.mileage_list, name='mileage_list' ),
    path('custom_mileage', CustomMileageListView.as_view() , name='custom_mileage' ),
    url(r'^mileage/create/$', MileageCreateView.as_view(), name='mileage_create'),
    url(r'^mileage/delete/(?P<pk>\d+)/', MileageDeleteView.as_view(), name='mileage_delete'),
    path('mileage/<int:pk>/edit/', MileageUpdateView.as_view(), name='mileage_update'),

    path('bicycles', BicycleListView.as_view(), name='bicycle_list'),
    path('bicycles/create', BicycleCreateView.as_view(), name='bicycle_create'),
    path('bicycles/<int:pk>/', BicycleUpdateView.as_view(), name='bicycle_update'),
    path('bicycles/<int:pk>/delete', BicycleDeleteView.as_view(), name='bicycle_delete'),

    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    
    # Kanopy app
    url(r'^kanopy$', kanopy_views.kanopy_home, name='kanopy_home'),
    url(r'^kanopy_table$', kanopy_views.kanopy_table, name='kanopy_table'),
    url(r'^kanopy_upload$', kanopy_views.model_form_upload, name='kanopy_upload'),
    # url(r'^kanopy_sample$', kanopy_views.sample_point_form_upload, name='kanopy_sample'),
    url(r'^kanopy_sample$', kanopy_views.addPointOnMap, name='kanopy_sample'),
    # url(r'^kanopy_sample$', kanopy_views.MapView.as_view(), name='kanopy_sample'),
    
    

    # Books app
    url(r'^books/$', books_views.book_list, name="book_list"),
    url(r'^books/create/$', books_views.book_create, name='book_create'),
    url(r'^books/(?P<pk>\d+)/update/$', books_views.book_update, name='book_update'),
    url(r'^books/(?P<pk>\d+)/delete/$', books_views.book_delete, name='book_delete'),
    
    # Accounts
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),

    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'^settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account'),
        
    # Boards 
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post'),
    url(r'^new_post/$', views.NewPostView.as_view(), name='new_post'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),
    # url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
