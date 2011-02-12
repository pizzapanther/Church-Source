import re

from django.conf import settings
from django import shortcuts
from django.template import RequestContext
from django import http

try:
  ADMIN_REMEMBER_QUERIES = settings.ADMIN_REMEMBER_QUERIES
  
except:
  ADMIN_REMEMBER_QUERIES = False
  
class Command:
  def __init__(self, func, *args, **kw):
    self.func = func
    self.args = args
    self.kw = kw
    
  def __call__(self, *args, **kw):
    args = self.args + args
    kw.update(self.kw)
    return self.func(*args, **kw)
    
def render_to_response (request, template, dictionary=None, context_instance=None, mimetype=None):
  if not context_instance:
    context_instance = RequestContext(request)
    
  return shortcuts.render_to_response(template, dictionary, context_instance, mimetype=mimetype)
  
class Shortcuts:
  def process_request (self, request):
    request.render_to_response = Command(render_to_response, request)
    request.task = request.REQUEST.get('task', '')
    request.ERROR_MESSAGE = 'There are errors in your request.'
    
    return None
    
class AdminQuery:
  def process_request (self, request):
    if ADMIN_REMEMBER_QUERIES:
      if request.method == 'GET':
        found = re.search("^/admin/(\S+)/(\S+)/$", request.path)
        clear = request.REQUEST.get('__clearqs', '')
        pop = request.REQUEST.get('pop', '')
        
        if found and pop != '1':
          key = 'aquery-%s-%s' % (found.group(1), found.group(2))
          
          if clear == '1':
            try:
              del request.session[key]
              
            except:
              pass
              
            return http.HttpResponseRedirect(request.path)
            
          if request.META['QUERY_STRING']:
            request.session[key] = request.META['QUERY_STRING']
            
          else:
            try:
              qs = request.session[key]
              
            except:
              pass
              
            else:
              return http.HttpResponseRedirect('%s?%s' % (request.path, qs))
              
    return None
    