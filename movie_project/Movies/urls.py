"""
URLs for the cars app.
"""
from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',

    url(r'^$',  views.MovieView.as_view(), name='Movies'),
)
