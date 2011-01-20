from django import shortcuts
from django.template import RequestContext

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
    
    return None
    