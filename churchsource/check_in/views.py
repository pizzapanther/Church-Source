import os
import re
import datetime
import urllib
import urlparse

from django import http
from django.conf import settings
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.core.files import File

import churchsource.check_in.models as cmodels
import churchsource.check_in.forms as cforms
import churchsource.people.models as pmodels
import churchsource.utils.face as face

@permission_required('check_in.add_checkin')
def face_check (request):
  return request.render_to_response('checkin/face_check.html', {})
  
@permission_required('check_in.add_checkin')
def terminal (request):
  can_create = request.user.has_perm('check_in.add_event')
  eforms = None
  now = datetime.datetime.now()
  events = cmodels.Event.objects.filter(start__year=now.year, start__month=now.month, start__day=now.day).filter(Q(end__isnull=True) | Q(end__gte=now))
  checked = []
  events_created = []
  message = ""
  touch = request.REQUEST.get('touch', '1')
  
  if request.task != '':
    for c in request.POST.getlist('event_check'):
      try:
        checked.append(int(c))
        
      except:
        pass
        
    if len(checked) == 0:
      message = "Sorry there are no events to check in for right now."
      
    if message == '':
      estr = ''
      for c in checked:
        estr += '%d-' % c
        
      estr = estr[:-1]
      if touch:
        estr += '-touch'
        
      return http.HttpResponseRedirect(reverse('cs_terminal_checkin', kwargs={'events': estr}))
      
  else:
    for e in events:
      checked.append(e.id)
      
  c = {'events': events, 'checked': checked, 'message': message, 'touch': False, 'touchon': touch}
  return request.render_to_response('checkin/terminal.html', c)
  
@permission_required('check_in.add_checkin')
def terminal_checkin (request, events='', touch=None):
  message = ''
  checkins = None
  code = None
  code_tags = []
  real_code_tags = []
  
  if request.task == 'Search':
    search = request.REQUEST.get('search', '')
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
          
        #households = pmodels.Household.objects.filter(q).filter(active=True, person__groups__gtype__in=['checkinc', 'checkina']).distinct()
        households = pmodels.Household.objects.filter(q).filter(active=True).distinct()
        
        if households.count() == 0:
          message = 'Nothing Found'
          if request.user.has_perm('people.add_household') and request.user.is_staff:
            message = 'Nothing Found'
            
        elif households.count() == 1:
          return http.HttpResponseRedirect('./?task=household&h=%d' % households[0].id)
          
        else:
          return request.render_to_response('checkin/terminal_choose.html', {'households': households, 'touch': touch})
          
  elif request.task == 'PicSearch':
    pic = request.REQUEST.get('pic', '')
    try:
      timg = pmodels.TempImage.objects.get(id=pic)
      
    except:
      message = 'Invalid Image.'
      
    else:
      households = face.find_households(settings.FACE_COM_HTTP + timg.image.url)
      timg.delete()
      if households:
        if len(households) == 1:
          return http.HttpResponseRedirect('./?task=household&h=%d' % households[0].id)
          
        else:
          return request.render_to_response('checkin/terminal_choose.html', {'households': households, 'touch': touch})
          
      else:
        message = 'Nothing Found'
        
  elif request.task == 'household':
    h = request.REQUEST.get('h', '')
    try:
      h = pmodels.Household.objects.get(id=h)
      
    except:
      return http.HttpResponseRedirect('./')
      
    else:
      now = datetime.datetime.now()
      events = cmodels.Event.objects.filter(id__in=events.split("-")).filter(Q(end__isnull=True) | Q(end__gte=now))
      return request.render_to_response('checkin/terminal_checkin.html', {'h': h, 'events': events, 'touch': touch})
      
  elif request.task == 'Check In':
    checkins = []
    events = cmodels.Event.objects.filter(id__in=[elem for elem in request.POST.getlist('events') if elem != ""])
    peeps = pmodels.Person.objects.filter(id__in=[elem for elem in request.POST.getlist('peeps') if elem != ""])
    pager = request.POST.get('pager', '')
    
    for e in events:
      if e.code:
        code = cmodels.gencode()
        break
        
    for p in peeps:
      mycode = code
      if p.is_adult():
        mycode = None
        
      ci = cmodels.CheckIn(person=p, code=mycode, pager=pager)
      ci.save()
      
      for e in events:
        #if e.eventgroup_set.filter(group__id__in=p.groups.all().values_list('id', flat=True)).count() > 0:
        ci.events.add(e)
        
      ci.extra_labels = range(0, int(request.POST.get('%d_extra_labels' % p.id, '0')))
      
      checkins.append(ci)
      code_tags.append(mycode)
      
    code_tags = [elem for elem in code_tags if elem is not None]
    if code:
      for i in range(0, (len(code_tags) + 1)/2):
        real_code_tags.append(code)
        
  c = {'message': message, 'checkins': checkins, 'code': code, 'code_tags': real_code_tags, 'touch': touch, 'submit_on_accept': True, 'scroll_off': True}
  return request.render_to_response('checkin/terminal_search.html', c)
  
@permission_required('check_in.can_generate_reports')
def reports (request):
  eids = request.REQUEST.getlist('event')
  format = request.REQUEST.get('format', 'print')
  with_adults = request.REQUEST.get('with_adults', '')
  
  events = cmodels.Event.objects.filter(id__in=eids)
  total = pmodels.Person.objects.filter(checkin__events__id__in=eids).distinct().order_by('id').count()
  
  return request.render_to_response('checkin/reports.html', {'events': events, 'total': total, 'with_adults': with_adults})
  
@permission_required('people.add_person')
def add_person (request, hhold=None):
  h = get_object_or_404(pmodels.Household, id=hhold)
  goback = request.REQUEST.get('goback', '')
  form = cforms.PersonForm()
  touch = False
  groups = request.REQUEST.getlist('groupid')
  groups = [elem for elem in groups if elem != ""]
  
  if re.search('-touch', goback):
    touch = True
    
  now = datetime.datetime.now()
  #tgroups = pmodels.Group.objects.filter(eventgroup__event__start__year=now.year, eventgroup__event__start__month=now.month, eventgroup__event__start__day=now.day).distinct()
  tgroups = pmodels.Group.objects.filter(Q(gtype='checkinc') | Q(gtype='checkina')).exclude(auth=True)
  if request.task == 'Submit':
    form = cforms.PersonForm(request.POST, {'groups': groups})
    
    if form.is_valid():
      p = form.save(commit=False)
      p.household = h
      p.save()
      for g in groups:
        p.groups.add(pmodels.Group.objects.get(id=g))
        
      return http.HttpResponseRedirect(goback)
      
  c = {'touch': touch, 'goback': goback, 'h': h, 'form': form, 'tgroups': tgroups, 'groups': groups}
  return request.render_to_response('checkin/add_person.html', c)
  
@permission_required('people.add_tempimage')
def temp_image (request):
  return request.render_to_response('checkin/temp_image.html', {})
  
@permission_required('people.add_tempimage')
def picnik (request, name=None):
  furl = request.REQUEST.get('file', '')
  ti = None
  if re.search("http://www.picnik", furl):
    f = urllib.urlopen(furl)
    
    fname = datetime.datetime.now().strftime("%a%d%b%Y%H%M%S%f.jpg")
    fp = os.path.join('/tmp', fname)
    fh = open(fp, 'wb')
    ti = pmodels.TempImage()
    while 1:
      data = f.read(64 * 2 ** 10)
      if data:
        fh.write(data)
        
      else:
        break
        
    f.close()
    fh.close()
    
    fh = File(open(fp, 'rb'))
    
    ti.image.save(fname, fh, save=True)
    ti.save()
    fh.close()
    
  return request.render_to_response('admin/people/tempimage/picnik.html', {'ti': ti, 'name': name})
  
@permission_required('people.add_person')
def edit_person (request, person=None):
  touch = False
  goback = request.REQUEST.get('goback', '')
  
  if re.search('-touch', goback):
    touch = True
    
  p = get_object_or_404(pmodels.Person, id=person)
  form = cforms.PersonForm(instance=p)
  groups = []
  for g in p.groups.all():
    groups.append(str(g.id))
    
  tgroups = pmodels.Group.objects.filter(gtype='checkinc')
  if request.task == 'Submit':
    form = cforms.PersonForm(request.POST, instance=p)
    groups = request.REQUEST.getlist('groupid')
    groups = [elem for elem in groups if elem != ""]
    if form.is_valid():
      p = form.save(commit=False)
      p.save()
      p.groups.clear()
      
      for g in groups:
        p.groups.add(pmodels.Group.objects.get(id=g))
        
      return http.HttpResponseRedirect(goback)
      
  c = {'touch': touch, 'goback': goback, 'p': p, 'form': form, 'tgroups': tgroups, 'groups': groups}
  return request.render_to_response('checkin/edit_person.html', c)
  
@permission_required('people.add_household')
def add_household (request):
  goback = request.REQUEST.get('goback', '')
  form = cforms.HouseholdForm(initial={'alerts': True})
  touch = False
  if re.search('-touch', goback):
    touch = True
    
  if request.task == 'Next':
    form = cforms.HouseholdForm(request.POST)
    if form.is_valid():
      p = form.save(commit=False)
      h = pmodels.Household(name=p.lname, first_visit=datetime.date.today())
      if form.cleaned_data['barcode']:
        h.barcode = form.cleaned_data['barcode']
        
      h.save()
      
      p.household = h
      p.save()
      
      url = urlparse.urlparse(goback)
      gourl = url.path + '?task=household&h=%d' % h.id
      return http.HttpResponseRedirect(gourl)
      
  c = {'form': form, 'goback': goback, 'touch': touch}
  return request.render_to_response('checkin/add_household.html', c)
  
