import random
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command (BaseCommand):
  args = ''
  help = 'Generates a secret key and adds it into your settings_local.py'
  
  def handle(self, *args, **options):
    secret_key = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    secret_path = os.path.normpath(os.path.join(settings.SPATH, 'settings_local.py'))
    fh = open(secret_path, 'a')
    fh.write("\nSECRET_KEY = '%s'\n" % secret_key)
    fh.close()
    
    print "Secret successfully added to %s" % secret_path
    