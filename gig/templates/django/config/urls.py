from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    # You'll want to replace this with your own index.
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'})
)

if settings.DEBUG:
    urlpatterns += patterns('', 
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    )