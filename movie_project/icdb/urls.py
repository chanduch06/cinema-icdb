"""
URLs for the icdb project.
"""
from django.conf.urls import patterns, include,url

from Movies.views import MovieView

urlpatterns = patterns('',
   url(r'^Movies/', include('Movies.urls')),

)

