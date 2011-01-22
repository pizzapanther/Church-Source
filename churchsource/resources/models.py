from django.db import models

class Room (models.Model):
  name = models.CharField('Name', max_length=150)
  
  def __unicode__ (self):
    return self.name
    
  class Meta:
    ordering = ('name',)
    