from django.contrib import admin

import churchsource.configuration.models as cmodels

class SettingAdmin (admin.ModelAdmin):
  list_display = ('skey', 'name', 'stype', '_value')
  list_filter = ('stype',)
  search_fields = ('name', 'skey', 'value')
  
admin.site.register(cmodels.Setting, SettingAdmin)
