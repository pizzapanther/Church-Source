import os
import sys
import csv
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django import forms
import django.contrib.localflavor.us.forms as usforms

import churchsource.people.models as pmodels

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 0)

class Command (BaseCommand):
  args = '<file_path_1 file_path_2 ...>'
  help = 'Import people/households from CSV file.'
  
  def parse_phone (self, txt):
    f = usforms.USPhoneNumberField()
    try:
      return f.clean(txt)
      
    except:
      return None
      
  def parse_email (self, txt):
    f = forms.EmailField()
    try:
      return f.clean(txt)
      
    except:
      return None
      
  def parse_bday (self, txt):
    try:
      dt = datetime.datetime.strptime(txt, '%d-%b-%y')
      return datetime.date(year=dt.year, month=dt.month, day=dt.day)
      
    except:
      return None
      
  def handle(self, *args, **options):
    for a in args:
      if not os.path.exists(a):
        raise CommandError('Invalid file: %s' % a)
        
    data = {}
    for a in args:
      fh = open(a, 'rb')
      reader = csv.reader(fh)
      for row in reader:
        if row[0] != 'Last Name':
          if data.has_key(row[10]):
            data[row[10]].append(row)
            
          else:
            data[row[10]] = [row,]
            
      fh.close()
      
    hcount = 0
    pcount = 0
    gcount = 0
    groups = {}
    
    for key in data.keys():
      peeps = data[key]
      h = pmodels.Household(name=peeps[0][0])
      print 'h', 
      h.save()
      hcount += 1
      addresses = {}
      
      for peep in peeps:
        p = pmodels.Person(
            lname=peep[0],
            fname=peep[1],
            household=h,
            bdate=self.parse_bday(peep[2]),
            email=self.parse_email(peep[5])
          )
        
        print 'p', 
        p.save()
        pcount += 1
        
        for gstr in peep[11].split(", "):
          if gstr != '' and gstr != '-':
            if not groups.has_key(gstr):
              groups[gstr] = pmodels.Group(name=gstr)
              groups[gstr].save()
              gcount += 1
              
            print 'g',
            p.groups.add(groups[gstr])
            
        phone = self.parse_phone(peep[4])
        if phone:
          ph = pmodels.Phone(person=p, number=phone)
          ph.save()
          print 'ph',
          
        if peep[8] != '' and peep[8] != '-':
          if peep[8] not in addresses.keys():
            addresses[peep[8]] = pmodels.Address(household=h, address1=peep[8], state=peep[7], city=peep[6], zipcode=peep[9], atype='home')
            addresses[peep[8]].save()
            print 'a',
            
      #if hcount > 10:
      #  break
      #  
    print "\n\nCreated: Household=%d People=%d Groups=%d" % (hcount, pcount, gcount)
    