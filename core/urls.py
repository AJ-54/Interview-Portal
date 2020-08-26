from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # re_path('', TemplateView.as_view(template_name="index.html")),
    url(r'^$', views.index_view, name = 'home'),
    url(r'^home/$', views.home_view, name = 'login'),
    url(r'^home/all_interviews/$', views.all_interviews_view, name = "all_interviews"),
    url(r'^home/create/$', views.create_view, name = "create"),
]

