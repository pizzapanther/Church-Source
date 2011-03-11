import re

from django.db.models import Q

from churchsource.people.models import Person

def format_id (i):
  if i < 10:
    return '%d     ' % i
    
  elif i < 100:
    return '%d    ' % i
    
  elif i < 1000:
    return '%d   ' % i
    
  elif i < 10000:
    return '%d  ' % i
    
  elif i < 100000:
    return '%d ' % i
    
  return '%d' % i
  
class PersonChannel (object):
  def get_query(self, q, request):
    qset = None
    
    for qs in re.split("\s+", q):
      if qset is None:
        qset = Person.objects.filter(Q(lname__icontains=qs) | Q(fname__icontains=qs))
        
      else:
        qset = qset.filter(Q(lname__icontains=qs) | Q(fname__icontains=qs))
        
    print qset.query
    return qset
    
  def format_item(self, obj):
    return unicode(obj)
    
  def format_result(self, obj):
    if obj.mname:
      return '%s: %s, %s %s' % (format_id(obj.id), obj.lname, obj.fname, obj.mname)
      
    else:
      return '%s: %s, %s' % (format_id(obj.id), obj.lname, obj.fname)
      
  def get_objects(self, ids):
    return Person.objects.filter(pk__in=ids)
    
class PersonChannelBdate (PersonChannel):
  def format_item(self, obj):
    if obj.bdate:
      return unicode(obj) + ' - ' + obj.birthday()
      
    return unicode(obj)
      