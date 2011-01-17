from django.db import models

import churchsource.people.models as pmodels

class Event (models.Model):
  name = models.CharField('Name', max_length=150)
  start = models.DateTimeField('Start')
  end = models.DateTimeField('End', blank=True, null=True)
  
  def __unicode__ (self):
    '%s - %d/%d/%d' % (self.name, self.start.month, self.start.day, self.start.year)
    
  class Meta:
    ordering = ('-start', 'name')
    
class CheckIn (models.Model):
  person = models.ForeignKey(pmodels.Person)
  
  cin = models.DateTimeField('Check In', auto_now_add=True)
  cout = models.DateTimeField('Check Out', blank=True, null=True)
  code = models.CharField('Sticker Code', max_length=4)
  
  events = models.ManyToManyField(Event)
  
  def __unicode__ (self):
    return cin.strftime('%m/%d/%Y %I:%M %p') + ': %s, %s' % (self.person.lname, self.person.fname)
    
  class Meta:
    ordering = ('-cin', 'person__lname', 'person__fname')
    