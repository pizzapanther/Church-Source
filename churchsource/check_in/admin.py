from django.contrib import admin

import churchsource.check_in.models as cmodels

class CheckInAdmin (admin.ModelAdmin):
  raw_id_fields = ('person', )
  list_display = ('cin', 'cout', 'person', 'code', '_Events')
  search_fields = ('person__fname', 'person__lname', 'code')
  list_filter = ('cin', 'cout')
  filter_horizontal = ('events',)
  
class EventAdmin (admin.ModelAdmin):
  list_display = ('name', 'start', 'end', 'code')
  list_filter = ('start',)
  search_fields = ('name',)
  date_hierarchy  = 'start'
  filter_horizontal = ('groups',)
  
admin.site.register(cmodels.Event, EventAdmin)
admin.site.register(cmodels.CheckIn, CheckInAdmin)
