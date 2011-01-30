import re
import datetime

from django import http
from django import forms
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

class EventGroupInline (admin.TabularInline):
  model = cmodels.EventGroup
  raw_id_fields = ('group', 'room')
  
class EventForm (forms.ModelForm):
  repeat = forms.ChoiceField(choices=(('', 'None'), ('day', 'Daily'), ('week', 'Weekly')), label="Repeat", required=False)
  repeat_times = forms.IntegerField(label="Number of Repeats", required=False)
  update_links = forms.ChoiceField(choices=(('me', 'Just this event'), ('all', 'All repeat events')), initial="me", label="Update", required=False)
  
  def clean_repeat (self):
    if self.cleaned_data['repeat']:
      if not self['repeat_times'].data or self['repeat_times'].data == '':
        raise forms.ValidationError('Please enter repeat number.')
        
    return self.cleaned_data['repeat']
    
  class Meta:
    model = cmodels.Event
    exclude = ('link',)
    
class EventAdmin (admin.ModelAdmin):
  list_display = ('name', 'start', 'end', 'code', 'attendance')
  list_filter = ('start',)
  search_fields = ('name',)
  date_hierarchy  = 'start'
  form = EventForm
  fieldsets = ((None, {'fields': ['name', 'code', 'start', 'end', ('repeat', 'repeat_times')]}),)
    
  inlines = [EventGroupInline,]
  actions = [gen_report, gen_report2]
  
  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for instance in instances:
      instance.save()
      obj = instance.event
      
    formset.save_m2m()
    
    if change:
      found = re.search('/(\d+)/$', request.path)
      obj = cmodels.Event.objects.get(id=found.group(1))
      if obj.link:
        if form.cleaned_data['update_links'] == 'all':
          for e in cmodels.Event.objects.filter(link=obj.link).exclude(id=obj.id):
            e.name = obj.name
            e.code = obj.code
            e.save()
            
            e.eventgroup_set.all().delete()
            for evg in obj.eventgroup_set.all():
              new_evg = cmodels.EventGroup(group=evg.group, room=evg.room, event=e)
              new_evg.save()
              
    else:
      increment = None
      r = form.cleaned_data['repeat_times']
      
      if form.cleaned_data['repeat'] == 'day':
        increment = datetime.timedelta(days=1)
        
      elif form.cleaned_data['repeat'] == 'week':
        increment = datetime.timedelta(days=7)
        
      if increment:
        start = obj.start
        end = obj.end
        
        obj.link = obj
        obj.save()
        
        for i in range(0, r):
          start = start + increment
          if end:
            end = end + increment
            
          new_obj = cmodels.Event(name=obj.name, code=obj.code, link=obj, start=start, end=end)
          new_obj.save()
          for evg in obj.eventgroup_set.all():
            new_evg = cmodels.EventGroup(group=evg.group, room=evg.room, event=new_obj)
            new_evg.save()
            
  def get_fieldsets(self, request, obj=None):
    if not re.search('add', request.path):
      if obj.link:
        return ((None, {'fields': ['name', 'code', 'start', 'end', 'update_links']}),)
        
      else:
        return ((None, {'fields': ['name', 'code', 'start', 'end']}),)
        
    return super(EventAdmin, self).get_fieldsets(request, obj=obj)
    
admin.site.register(cmodels.Event, EventAdmin)
admin.site.register(cmodels.CheckIn, CheckInAdmin)
