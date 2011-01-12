from django.contrib import admin
from django import http
from django import forms
from django.db import models

import churchsource.people.models as pmodels
import churchsource.people.widgets as widgets

class PersonInline (admin.StackedInline):
  model = pmodels.Person
  fieldsets = (
    (None, {
      'fields': (('fname', 'lname'), ('email', 'alerts'), ('gender', 'role'), ('bdate', 'ddate'), 'allergies', 'image', 'details')
    }),
  )
  readonly_fields = ('details',)
  
  formfield_overrides = {models.ImageField: {'widget': widgets.WebcamModal},}
  
class AddressInline (admin.StackedInline):
  model = pmodels.Address
  extra = 1
  fieldsets = (
    (None, {
      'fields': ('address1','address2', ('city','state'), ('atype', 'zipcode'), 'notes')
    }),
  )

class HouseholdAdmin (admin.ModelAdmin):
  save_on_top = True
  
  list_display = ('name', 'status', 'anniversary_', 'active', 'first_visit', 'members')
  search_fields = ('name', 'person__fname', 'person__lname', 'person__email')
  list_filter = ('active', 'status', 'first_visit')
  date_hierarchy  = 'anniversary'
  
  formfield_overrides = {models.ImageField: {'widget': widgets.WebcamModal},}
  
  inlines = (PersonInline, AddressInline)
  
class PhoneInline (admin.TabularInline):
  model = pmodels.Phone
  
class PersonAdmin (admin.ModelAdmin):
  list_select_related = True
  list_display = ('lname', 'fname', 'email', 'birthday', 'gender', 'role', 'active', 'edit_household')
  search_fields = ('fname', 'lname', 'email', 'household__name')
  list_filter = ('gender', 'role')
  date_hierarchy  = 'bdate'
  raw_id_fields = ('household',)
  
  formfield_overrides = {models.ImageField: {'widget': widgets.WebcamModal},}
  
  inlines = (PhoneInline, )
  
  fieldsets = (
    (None, {
      'fields': ('household', ('fname', 'lname'), ('mname', 'email', 'alerts'), ('gender', 'role'), ('bdate', 'ddate'), 'allergies', 'image')
    }),
  )
  
  def response_add (self, request, obj, post_url_continue='../%s/'):
    ret = super(PersonAdmin, self).response_add(request, obj, post_url_continue=post_url_continue)
    if request.POST.has_key("_gohousehold"):
      return http.HttpResponseRedirect("../../household/%d/" % obj.household.id)
      
    return ret
    
  def response_change (self, request, obj):
    ret = super(PersonAdmin, self).response_change(request, obj)
    if request.POST.has_key("_gohousehold"):
      return http.HttpResponseRedirect("../../household/%d/" % obj.household.id)
      
    return ret
    
class PhoneAdmin (admin.ModelAdmin):
  list_select_related = True
  list_display = ('person', 'description', 'number', 'alerts')
  search_fields = ('person__fname', 'person__lname', 'person__email', 'person__household__name', 'number')
  list_filter = ('alerts', 'type1', 'type2')
  
class TIAdmin (admin.ModelAdmin):
  list_display = ('image', 'ts')
  
admin.site.register(pmodels.Household, HouseholdAdmin)
admin.site.register(pmodels.Person, PersonAdmin)
admin.site.register(pmodels.Phone, PhoneAdmin)
admin.site.register(pmodels.TempImage, TIAdmin)
