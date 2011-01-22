import datetime

from django import http
from django.db.models import Q
from django.core.urlresolvers import reverse

import churchsource.check_in.models as cmodels
import churchsource.check_in.forms as cforms

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
            pass
            #create event
            #events_created.append(e.id)
            
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
  return request.render_to_response('checkin/terminal_checkin.html', {})
  
def reports (request):
  pass
  
