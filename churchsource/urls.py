import os

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^churchsource/', include('churchsource.foo.urls')),
    
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^', include('sorl.thumbnail.urls')),
)

if settings.DEBUG:
  urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': os.path.join(settings.SPATH, 'static'), 'show_indexes': True}),
  )
  