from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()





urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.urls')),
	(r'^forum/', include('pybb.urls', namespace='pybb')),
    (r'^$', direct_to_template, 
	{ 'template': 'index.html' }, 'index'),
			
)
