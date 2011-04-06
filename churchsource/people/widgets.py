from django.utils.safestring import mark_safe
from django.conf import settings
from django.template.loader import render_to_string
from django import forms

class WebcamModal (forms.FileInput):
  def __init__ (self, *args, **kw):
    super(WebcamModal, self).__init__(*args, **kw)
    self.template = 'admin/widget_webcam_modal.html'
    
  class Media:
    js = ('js/jquery-1.4.4.min.js', 'js/modal/js/jquery.simplemodal.js', 'picnik/picnikbox_2_0.js')
    css = {'all': ('js/modal/css/basic.css', 'picnik/picnikbox_2_0.css')}
    
  def render(self, name, value, attrs=None):
    try:
      img = getattr(value.instance, 'image')
      
    except:
      img = None
      
    try:
      household = getattr(value.instance, 'household')
      
    except:
      household = None
      
    c = {
         'name':name,
         'img': img,
         'household': household,
         'media': settings.MEDIA_URL,
         'w': settings.WEBCAM_WIDTH,
         'h': settings.WEBCAM_HEIGHT,
	 'w_real': settings.WEBCAM_WIDTH_REAL,
         'h_real': settings.WEBCAM_HEIGHT_REAL,
         'picnik': settings.PICNIK_KEY,
         'http': settings.HTTP_BASE
        }
    return mark_safe(render_to_string(self.template, c))
    
class Webcam (forms.FileInput):
	class Media:
		js = ('jpegcam/webcam.js',)
		
	def render(self, name, value, attrs=None):
		try:
			img = getattr(value.instance, name)
			
		except:
			img = None
			
		c = {'name':name, 'img': img, 'media': settings.MEDIA_URL, 'w': settings.WEBCAM_WIDTH, 'h': settings.WEBCAM_HEIGHT, 'w_real': settings.WEBCAM_WIDTH_REAL, 'h_real': settings.WEBCAM_HEIGHT_REAL,}
		return mark_safe(render_to_string('admin/widget_webcam.html', c))
