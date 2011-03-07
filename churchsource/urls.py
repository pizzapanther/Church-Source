import os

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    ('^favicon.ico$', 'django.views.generic.simple.redirect_to', {'url': '%sfavicon.ico' % settings.MEDIA_URL}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
)

urlpatterns += patterns('churchsource.people.views',
  url(r'^jpegcam/$', 'jpegcam_admin', name='cs_jpegcam'),
  url(r'^checkin/reports/group/$', 'reports', name='cs_group_report')
)

urlpatterns += patterns('churchsource.check_in.views',
  url(r'^checkin/terminal/$', 'terminal', name='cs_terminal'),
  url(r'^checkin/terminal/events-(?P<events>.*)-(?P<touch>touch)/$', 'terminal_checkin', name='cs_terminal_checkin_touch'),
  url(r'^checkin/terminal/events-(?P<events>.*)/$', 'terminal_checkin', name='cs_terminal_checkin'),
  url(r'^checkin/reports/$', 'reports', name='cs_reports'),
  url(r'^checkin/add_household/$', 'add_household', name='cs_add_hhold'),
  url(r'^checkin/add_person/(?P<hhold>\d+)/$', 'add_person', name='cs_add_person'),
  url(r'^checkin/edit_person/(?P<person>\d+)/$', 'edit_person', name='cs_edit_person'),
  url(r'^checkin/temp_image/$', 'temp_image', name='cs_temp_image'),
)

if settings.DEBUG:
  urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': os.path.join(settings.SPATH, 'static'), 'show_indexes': True}),
  )
  
if settings.THUMBNAIL_DUMMY:
  urlpatterns += patterns('',
    (r'^', include('sorl.thumbnail.urls')),
  )
  