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
from django.urls import re_path, path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from accounts import views as accounts_views
from boards import views
from plotter import views as plotter_views
from books import views as books_views

from bikemileage.views import (
    CustomMileageListView,
    MileageCreateView,
    MileageUpdateView,
    MileageDeleteView,
)
from bikemileage.views import (
    BicycleListView,
    BicycleCreateView,
    BicycleUpdateView,
    BicycleDeleteView,
)

urlpatterns = [
    # For soils in depth
    path("", include("plotter.urls")),
    # Kanopy app
    path("", include("kanopy.urls")),
    # wisccc app
    path("", include("wisccc.urls")),
    # glccp app
    path("", include("glccp.urls")),
    path("contact/", books_views.ContactView.as_view(), name="contact"),
    path("success/", books_views.SuccessView.as_view(), name="success"),
    # bikemileage App
    # re_path(r'^mileage/$',mileage_views.mileage_list, name='mileage_list' ),
    path("custom_mileage", CustomMileageListView.as_view(), name="custom_mileage"),
    path("mileage/create/", MileageCreateView.as_view(), name="mileage_create"),
    re_path(
        r"^mileage/delete/(?P<pk>\d+)/",
        MileageDeleteView.as_view(),
        name="mileage_delete",
    ),
    path("mileage/<int:pk>/edit/", MileageUpdateView.as_view(), name="mileage_update"),
    path("bicycles", BicycleListView.as_view(), name="bicycle_list"),
    path("bicycles/create", BicycleCreateView.as_view(), name="bicycle_create"),
    path("bicycles/<int:pk>/", BicycleUpdateView.as_view(), name="bicycle_update"),
    path(
        "bicycles/<int:pk>/delete", BicycleDeleteView.as_view(), name="bicycle_delete"
    ),
    # re_path(r"^signup/$", accounts_views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Books app
    path("", books_views.home, name="home"),
    path("books/", books_views.book_list, name="book_list"),
    path("books/create/", books_views.book_create, name="book_create"),
    path("books/<int:pk>/update/", books_views.book_update, name="book_update"),
    path("books/<int:pk>/delete/", books_views.book_delete, name="book_delete"),
    # Accounts
    path(
        "settings/password/",
        auth_views.PasswordChangeView.as_view(template_name="password_change.html"),
        name="password_change",
    ),
    path(
        "settings/password/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html",
            email_template_name="password_reset_email.html",
            subject_template_name="password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        r"reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "settings/account/",
        accounts_views.UserUpdateView.as_view(),
        name="my_account",
    ),
    # Boards
    path("boards", views.BoardListView.as_view(), name="home_boards"),
    path(
        "boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/",
        views.PostUpdateView.as_view(),
        name="edit_post",
    ),
    path("new_post/", views.NewPostView.as_view(), name="new_post"),
    path(
        "boards/<int:pk>/topics/<int:topic_pk>/reply/",
        views.reply_topic,
        name="reply_topic",
    ),
    path(
        "boards/<int:pk>/topics/<int:topic_pk>/",
        views.PostListView.as_view(),
        name="topic_posts",
    ),
    # re_path(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    path("boards/<int:pk>/", views.TopicListView.as_view(), name="board_topics"),
    path("boards/<int:pk>/new/", views.new_topic, name="new_topic"),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
