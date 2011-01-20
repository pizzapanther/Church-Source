import datetime

from django.db.models import Q

import churchsource.check_in.models as cmodels
import churchsource.check_in.forms as cforms

def terminal (request, events=None):
  if events:
    return request.render_to_response('checkin/terminal_checkin.html', {})
    
  else:
    can_create = request.user.has_perm('check_in.add_event')
    eforms = None
    
    if can_create:
      eforms = cforms.EventFormSet()
      
    now = datetime.datetime.now()
    events = cmodels.Event.objects.filter(start__year=now.year, start__month=now.month, start__day=now.day).filter(Q(end__isnull=True) | Q(end__gte=now))
    
    c = {'can_create': can_create, 'eforms': eforms, 'events': events}
    
    return request.render_to_response('checkin/terminal.html', c)
    
def reports (request):
  pass
  
