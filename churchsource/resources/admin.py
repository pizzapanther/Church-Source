from django.contrib import admin

import churchsource.resources.models as rmodels

class RoomAdmin (admin.ModelAdmin):
  list_display = ('name',)
  search_fields = ('name',)
  
admin.site.register(rmodels.Room, RoomAdmin)
