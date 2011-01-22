import re
import datetime

from django import http
from django.db.models import Q
from django.core.urlresolvers import reverse

import churchsource.check_in.models as cmodels
import churchsource.check_in.forms as cforms
import churchsource.people.models as pmodels

def terminal (request):
  can_create = request.user.has_perm('check_in.add_event')
  eforms = None
  now = datetime.datetime.now()
  events = cmodels.Event.objects.filter(start__year=now.year, start__month=now.month, start__day=now.day).filter(Q(end__isnull=True) | Q(end__gte=now))
  checked = []
  events_created = []
  message = ""
  
  if request.task != '':
    for c in request.POST.getlist('event_check'):
      try:
        checked.append(int(c))
        
      except:
        pass
        
    if can_create:
      eforms = cforms.EventFormSet(request.POST)
      if eforms.is_valid():
        for eform in eforms.forms:
          if len(eform.cleaned_data.keys()) > 0:
            today = datetime.date.today()
            start = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=eform.cleaned_data['start'].hour, minute=eform.cleaned_data['start'].minute)
            end = None
            if eform.cleaned_data['end']:
              end = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=eform.cleaned_data['end'].hour, minute=eform.cleaned_data['end'].minute)
              
            e = cmodels.Event(name=eform.cleaned_data['name'], start=start, end=end)
            e.save()
            events_created.append(e.id)
            
        if len(checked) + len(events_created) == 0:
          message = "Sorry there are no events to check in for right now."
          
      else:
        message = request.ERROR_MESSAGE
        
    else:
      if len(checked) == 0:
        message = "Sorry there are no events to check in for right now."
        
    if message == '':
      estr = ''
      for c in checked:
        estr += '%d-' % c
        
      for c in events_created:
        estr += '%d-' % c
        
      estr = estr[:-1]
      return http.HttpResponseRedirect(reverse('cs_terminal_checkin', kwargs={'events': estr}))
      
  else:
    if can_create:
      eforms = cforms.EventFormSet()
      
    for e in events:
      checked.append(e.id)
      
  c = {'can_create': can_create, 'eforms': eforms, 'events': events, 'checked': checked, 'message': message}
  return request.render_to_response('checkin/terminal.html', c)
  
def terminal_checkin (request, events=''):
  message = ''
  checkins = None
  code = None
  code_tags = []
  real_code_tags = []
  
  if request.task == 'Search':
    search = request.POST.get('search', '')
    if re.search('^\s*$', search):
      message = 'Please fill in a search term.'
      
    else:
      search_fields = ('name', 'barcode', 'person__fname', 'person__mname', 'person__lname')
      q = None
      for s in search_fields:
        if s == 'barcode':
          myq = Q(**{s + '__exact': search})
          
        else:
          myq = Q(**{s + '__icontains': search})
          
        if q:
          q = q | myq
          
        else:
          q = myq
          
        households = pmodels.Household.objects.filter(q).filter(active=True, person__groups__gtype__in=['checkinc', 'checkina']).distinct()
        if households.count() == 0:
          message = 'Nothing Found'
          
        elif households.count() == 1:
          return http.HttpResponseRedirect('./?task=household&h=%d' % households[0].id)
          
        else:
          return request.render_to_response('checkin/terminal_choose.html', {'households': households})
          
  elif request.task == 'household':
    h = request.REQUEST.get('h', '')
    try:
      h = pmodels.Household.objects.get(id=h)
      
    except:
      return http.HttpResponseRedirect('./')
      
    else:
      now = datetime.datetime.now()
      events = cmodels.Event.objects.filter(id__in=events.split("-")).filter(Q(end__isnull=True) | Q(end__gte=now))
      return request.render_to_response('checkin/terminal_checkin.html', {'h': h, 'events': events})
      
  elif request.task == 'Check In':
    checkins = []
    events = cmodels.Event.objects.filter(id__in=[elem for elem in request.POST.getlist('events') if elem != ""])
    peeps = pmodels.Person.objects.filter(id__in=[elem for elem in request.POST.getlist('peeps') if elem != ""])
    
    for e in events:
      if e.code:
        code = cmodels.gencode()
        break
        
    for p in peeps:
      mycode = code
      if p.is_adult():
        mycode = None
        
      ci = cmodels.CheckIn(person=p, code=mycode)
      ci.save()
      for e in events:
        ci.events.add(e)
        
      checkins.append(ci)
      code_tags.append(mycode)
      
    code_tags = [elem for elem in code_tags if elem is not None]
    if code:
      for i in range(0, (len(code_tags) + 1)/2):
        real_code_tags.append(code)
        
  return request.render_to_response('checkin/terminal_search.html', {'message': message, 'checkins': checkins, 'code': code, 'code_tags': real_code_tags})
  
def reports (request):
  pass
  
