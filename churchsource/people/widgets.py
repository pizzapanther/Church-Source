from django.utils.safestring import mark_safe
from django.conf import settings
from django.template.loader import render_to_string
from django import forms

class WebcamModal (forms.FileInput):
	class Media:
		js = ('js/jquery-1.4.4.min.js', 'js/modal/js/jquery.simplemodal.js')
		css = {'all': ('js/modal/css/basic.css',)}
		
	def render(self, name, value, attrs=None):
		try:
			img = getattr(value.instance, 'image')
			
		except:
			img = None
			
		print img
		c = {'name':name, 'img': img, 'media': settings.MEDIA_URL, 'w': settings.WEBCAM_WIDTH, 'h': settings.WEBCAM_HEIGHT}
		return mark_safe(render_to_string('admin/widget_webcam_modal.html', c))
		
class Webcam (forms.FileInput):
	class Media:
		js = ('jpegcam/webcam.js',)
		
	def render(self, name, value, attrs=None):
		try:
			img = getattr(value.instance, name)
			
		except:
			img = None
			
		c = {'name':name, 'img': img, 'media': settings.MEDIA_URL, 'w': settings.WEBCAM_WIDTH, 'h': settings.WEBCAM_HEIGHT}
		return mark_safe(render_to_string('admin/widget_webcam.html', c))