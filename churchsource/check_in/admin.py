from django import http
from django.contrib import admin
from django.core.urlresolvers import reverse

import churchsource.check_in.models as cmodels

class CheckInAdmin (admin.ModelAdmin):
  raw_id_fields = ('person', )
  list_display = ('cin', 'cout', 'person', 'code', '_Events')
  search_fields = ('person__fname', 'person__lname', 'code')
  list_filter = ('cin', 'cout')
  filter_horizontal = ('events',)
  
def gen_report (modeladmin, request, queryset, format='print'):
  qs = ''
  for e in queryset:
    qs += '&event=%d' % e.id
    
  return http.HttpResponseRedirect('%s?format=%s%s' % (reverse('cs_reports'), format, qs))
  
gen_report.short_description = "Generate Print Report"

def gen_report2 (modeladmin, request, queryset):
  return gen_report(modeladmin, request, queryset, format='csv')
  
gen_report2.short_description = "Generate Spreadsheet Report"

class EventAdmin (admin.ModelAdmin):
  list_display = ('name', 'start', 'end', 'code', 'attendance')
  list_filter = ('start',)
  search_fields = ('name',)
  date_hierarchy  = 'start'
  filter_horizontal = ('groups',)
  
  actions = [gen_report, gen_report2]
  
admin.site.register(cmodels.Event, EventAdmin)
admin.site.register(cmodels.CheckIn, CheckInAdmin)
