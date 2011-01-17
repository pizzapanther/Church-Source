from django.contrib import admin

import churchsource.check_in.models as cmodels

class CheckInAdmin (admin.ModelAdmin):
  raw_id_fields = ('person', )
  
admin.site.register(cmodels.Event)
admin.site.register(cmodels.CheckIn, CheckInAdmin)
