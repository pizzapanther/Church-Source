import os
import sys
import csv
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django import forms
import django.contrib.localflavor.us.forms as usforms
import django.contrib.auth.models as amodels
from django.contrib.contenttypes.models import ContentType

import churchsource.people.models as pmodels

NEW_GROUPS = {
  'UnManned Check In': [
    "check_in.add_checkin", "check_in.change_checkin", "people.add_address", "people.add_household",
    "people.add_person", "people.add_phone", "people.add_tempimage", "people.delete_tempimage"
  ],
  'Manned Check In': [
    "check_in.add_checkin", "check_in.change_checkin", "check_in.can_generate_reports", "check_in.add_event",
    "people.add_address", "people.change_address", "people.delete_address", "people.add_household",
    "people.change_household", "people.add_person", "people.change_person", "people.add_phone",
    "people.change_phone", "people.delete_phone", "people.add_tempimage", "people.delete_tempimage"
  ]
}

class Command (BaseCommand):
  args = ''
  help = 'Load Default Groups'
  
  def handle(self, *args, **options):
    try:
      ct = ContentType.objects.get(app_label='check_in', model='checkin')
      
    except:
      print "Re-Run migration again, content type hooks not executed."
      sys.exit(1)
      
    for key in NEW_GROUPS.keys():
      g = amodels.Group(name=key)
      g.save()
      for p in NEW_GROUPS[key]:
        temp = p.split('.')
        
        if temp[1] == 'can_generate_reports':
          ct = ContentType.objects.get(app_label=temp[0], model='checkin')
          
        else:
          temp2 = temp[1].split("_")
          ct = ContentType.objects.get(app_label=temp[0], model=temp2[1])
          
        g.permissions.add(amodels.Permission.objects.get(codename=temp[1], content_type=ct))
        