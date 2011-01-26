from django.contrib import admin
from django import http
from django import forms
import time

from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile

import churchsource.people.models as pmodels
import churchsource.people.widgets as widgets

class PersonInline (admin.StackedInline):
  model = pmodels.Person
  
  filter_horizontal = ('groups',)
  
  fieldsets = (
    (None, {
      'fields': (('fname', 'lname'), ('email', 'alerts'), ('gender', 'role'), ('bdate', 'ddate'), 'allergies', 'groups', 'image', 'image_temp', 'details')
    }),
  )
  readonly_fields = ('details',)
  raw_id_fields = ('image_temp', )
  
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
  raw_id_fields = ('image_temp', )
  
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
  raw_id_fields = ('household', 'image_temp')
  
  formfield_overrides = {models.ImageField: {'widget': widgets.WebcamModal},}
  
  inlines = (PhoneInline, )
  
  filter_horizontal = ('groups',)
  
  fieldsets = (
    (None, {
      'fields': ('household', ('fname', 'lname'), ('mname', 'alerts', 'email'), ('gender', 'role'), ('bdate', 'ddate'), 'allergies', 'groups', 'image', 'image_temp')
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
  list_display = ('image', 'view', 'ts')
  formfield_overrides = {models.ImageField: {'widget': widgets.Webcam},}
  
class GroupAdminInline (admin.TabularInline):
  model = pmodels.GroupAdmin
  raw_id_fields = ('person',)
  
class GroupMemberAdmin (admin.TabularInline):
  model = pmodels.Person.groups.through
  raw_id_fields = ('person', )
  verbose_name = "Member"
  verbose_name_plural = "Members"
  
class GroupAdmin (admin.ModelAdmin):
  list_display = ('name', 'gtype', 'room')
  list_filter = ('gtype',)
  search_fields = ('name',)
  raw_id_fields = ('room',)
  
  inlines = (GroupAdminInline, GroupMemberAdmin)
  
admin.site.register(pmodels.Household, HouseholdAdmin)
admin.site.register(pmodels.Person, PersonAdmin)
admin.site.register(pmodels.Phone, PhoneAdmin)
admin.site.register(pmodels.TempImage, TIAdmin)
admin.site.register(pmodels.Group, GroupAdmin)
