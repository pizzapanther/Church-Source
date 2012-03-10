#!/usr/bin/env python

import sys
import os
import argparse
import subprocess
import logging
import logging.handlers
import socket
import time
import functools
import signal
import traceback
from cStringIO import StringIO
import cPickle as pickle

import django.core.handlers.wsgi

import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import tornado.web
import tornado.options
import tornado.autoreload

import daemon

MYPATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, MYPATH)
sys.path.insert(0, os.path.abspath(os.path.join(MYPATH, '..')))

def exc_hook (t, v, trace):
  logging.exception('Error Information')
  logging.exception('Type: ' + str(t))
  logging.exception('Value: ' + str(v))
  
  fh = StringIO()
  traceback.print_exception(t, v, trace, file=fh)
  logging.exception(fh.getvalue())
  fh.close()
  
class StaticMedia(tornado.web.StaticFileHandler):
  def get_cache_time(self, path, modified, mime_type):
    return self.CACHE_MAX_AGE
    
def start_loop (args):
  os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'
  
  from django.conf import settings
  
  if not os.path.exists(settings.WORKING_DIR):
    os.makedirs(settings.WORKING_DIR)
    
  p = {'pid': os.getpid(), 'args': args}
  output = open(settings.PKLPATH, 'wb')
  pickle.dump(p, output)
  output.close()
  
  if not os.path.exists(settings.LOG_DIR):
    os.makedirs(settings.LOG_DIR)
    
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
  
  if args.logging:
    tornado.options.enable_pretty_logging()
    
  else:
    fileLogger = logging.handlers.RotatingFileHandler(filename=settings.LOGPATH, maxBytes=1024*1024, backupCount=9)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fileLogger.setFormatter(formatter)
    logger.addHandler(fileLogger)
    sys.excepthook = exc_hook
    
  wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
  application = tornado.web.Application([
    (r"/static/(.*)", StaticMedia, {'path': settings.MEDIA_ROOT}),
    (r".*", tornado.web.FallbackHandler, {'fallback': wsgi_app}),
  ], debug=settings.DEBUG, gzip=True)
  
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(settings.HTTP_PORT)
  
  io = tornado.ioloop.IOLoop.instance()
  io.start()
  
def stop_loop ():
  os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'
  
  from django.conf import settings
  
  pkl = open(settings.PKLPATH, 'rb')
  p = pickle.load(pkl)
  pkl.close()
  
  os.kill(p['pid'], signal.SIGKILL)
  return p['args']
  
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='CultureMap built in Web Server')
  parser.add_argument('-l', '--logging', action='store_true', dest='logging', help='Log to screen instead of file logging.')
  parser.add_argument('-f', '--foreground', action='store_true', dest='foreground', help='Run in foreground instead of as a daemon.')
  parser.add_argument('action', nargs=1, help='start|stop|restart')
  
  args = parser.parse_args()
  
  if 'stop' in args.action or 'restart' in args.action:
    print "Stopping Web Server ...",
    oldargs = stop_loop()
    if 'restart' in args.action:
      args = oldargs
      
    print "Done"
    
  if 'start' in args.action or 'restart' in args.action:
    os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'
    from django.conf import settings
    
    if args.foreground:
      start_loop(args)
      
    else:
      print "Starting Web Server ...",
      with daemon.DaemonContext():
        start_loop(args)
        
