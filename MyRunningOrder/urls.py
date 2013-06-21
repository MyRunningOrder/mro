from django.conf.urls import patterns, include, url

from django.http import HttpResponseRedirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyRunningOrder.views.home', name='home'),
    # url(r'^MyRunningOrder/', include('MyRunningOrder.foo.urls')),
   
    url(r'^$', lambda r : HttpResponseRedirect('choosesomeacts/')),
    url(r'^choosesomeacts/', include('choosesomeacts.urls')),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root':'static/'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
