import random
import datetime

from django.db import models
from django.db.models import Q
from django.core.urlresolvers import reverse

import churchsource.people.models as pmodels
import churchsource.resources.models as rmodels

class Event (models.Model):
  name = models.CharField('Name', max_length=150)
  start = models.DateTimeField('Start')
  end = models.DateTimeField('End', blank=True, null=True)
  code = models.BooleanField('Needs Check In Code', default=True)
  link = models.ForeignKey('self', blank=True, null=True)
  
  def __unicode__ (self):
    return '%s - %d/%d/%d' % (self.name, self.start.month, self.start.day, self.start.year)
    
  def attendance (self):
    ret = '<strong>Child Groups:</strong> <a href="%s?event=%d" target="_blank">Print Report</a>' % (reverse('cs_reports'), self.id)
    ret += '<div style="padding-top: 3px;"><strong>Child and Adult:</strong> <a href="%s?event=%d&with_adults=1" target="_blank">Print Report</a></div>' % (reverse('cs_reports'), self.id)
    return ret
    
  attendance.allow_tags = True
  
  class Meta:
    ordering = ('-start', 'name')
    
class EventGroup (models.Model):
  event = models.ForeignKey(Event)
  group = models.ForeignKey(pmodels.Group, limit_choices_to=Q(gtype='checkinc') | Q(gtype='checkina'))
  room = models.ForeignKey(rmodels.Room, blank=True, null=True)
  
  def __unicode__ (self):
    if self.room:
      return "%s - %s" % (self.group.name, self.room.name)
      
    else:
      return self.group.name
      
  class Meta:
    ordering = ('group', 'room')
    
class CheckIn (models.Model):
  person = models.ForeignKey(pmodels.Person)
  
  cin = models.DateTimeField('Check In', auto_now_add=True)
  cout = models.DateTimeField('Check Out', blank=True, null=True)
  code = models.CharField('Sticker Code', max_length=4, blank=True, null=True)
  pager = models.CharField('Pager', max_length=75, blank=True, null=True)
  printed = models.BooleanField(default=True)
  
  events = models.ManyToManyField(Event)
  
  def __unicode__ (self):
    return self.cin.strftime('%m/%d/%Y %I:%M %p') + ': %s, %s' % (self.person.lname, self.person.fname)
    
  def is_authorized (self):
    for e in self.events.all():
      for evg in e.eventgroup_set.all():
        for g in self.person.groups.all():
          if g.id == evg.group.id:
            if evg.group.auth:
              return True
              
    return False
    
  def _Events (self):
    ret = ''
    for e in self.events.all():
      ret += e.name + ', '
      
    return ret[:-2]
     
  class Meta:
    ordering = ('-cin', 'person__lname', 'person__fname')
    permissions = (("can_generate_reports", "Can generate check in reports"),)
    
def gencode ():
  today = datetime.date.today()
  while 1:
    code = ''
    for i in range(0,4):
      code += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789')
      
    if CheckIn.objects.filter(code=code, cin__year=today.year, cin__month=today.month, cin__day=today.day).count() == 0:
      break
      
  return code
  
