from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

class TouchBox (forms.CheckboxInput):
  def render(self, name, value, attrs=None):
    if self.check_test(self.attrs['tvalue']):
      ret = '<input type="checkbox" id="check_%s" checked="checked"/>' % name
      ret += '<input type="hidden" name="%s" id="check_%s_hidden" value="%s"/>' % (name, name, self.attrs['tvalue'])
      
    else:
      ret = '<input type="checkbox" id="check_%s"/>' % name
      ret += '<input type="hidden" name="%s" id="check_%s_hidden" value=""/>' % (name, name)
      
    ret += '<label onclick="toggle_check(\'check_%s\', \'%s\')" for="check_%s" id="check_%s_label">' %  (name, self.attrs['tvalue'], name, name)
    
    if self.check_test(self.attrs['tvalue']):
      ret += '<img src="%simg/checked.png" alt=""/> %s</label>' % (settings.MEDIA_URL, self.attrs['label'])
      
    else:
      ret += '<img src="%simg/unchecked.png" alt=""/> %s</label>' % (settings.MEDIA_URL, self.attrs['label'])
      
    ret += '<script type="text/javascript">$(document).ready(function () { $( "#check_%s" ).button(); });</script>' % name
    
    return mark_safe(ret)
    