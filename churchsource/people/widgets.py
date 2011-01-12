import base64, zlib

from django import forms
from django.utils.safestring import mark_safe
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

class WebcamWidget (forms.FileInput):
	pass
	
class WebcamWidget2 (forms.FileInput):
	'''
	Use in place of FileInput widget to enable interactive snapping of pictures using
	a webcam. The widget embeds a Flash application that interfaces with the native webcam.

	Constructor Arguments:
		attrs -- is a dictionary of attributes. For this widget, 'fallbackImageAttr' is the 
			name of an attribute of an instance to use as an image url if there is no 
			stored image. Use for things like gravatar.com.

	'''
	name = None
	file = None

	def render(self, name, value, attrs=None):
		try:
			url = getattr( value.instance, name ).url
		except (ValueError,AttributeError):
			try:
				url = getattr( value.instance, self.attrs['fallbackImageAttr'] )
			except (AttributeError,KeyError):
				url = ''

		return mark_safe(u'''
			<script type="text/javascript">
			<!--
				function %(name)sCallback(base64){
					var i = document.getElementById('id_%(name)s');
					i.type = 'hidden';
					i.value = base64;

					// See http://en.wikipedia.org/wiki/Data_URI_scheme
					// doesn't work in IE 7 or lower. Darn.
					var p = document.getElementById('%(name)s_img');
					p.src = 'data:image/jpeg;base64,' + base64; 
				}
			-->
			</script>
			<img src="%(url)s" id="%(name)s_img" class="personPhoto" style="float: left; max-width: 400px; max-height: 400px;" />
			<object type="application/x-shockwave-flash" 
				data="%(media)s/webcam/webcam.swf" 
				width="370" height="350"
				style="float:left;">
				<param name="flashVars" value="callback=%(name)sCallback" />
			</object>
			<input id="id_%(name)s" name="%(name)s" type="file" />
			''' % {'name':name, 'media':settings.MEDIA_URL, 'url':url}
		)

	def value_from_datadict(self,data,files,name):
		if self.file: return self.file

		if name in files:
			return super(WebcamWidget,self).value_from_datadict(data,files,name)
		elif data[name]:
			photo = base64.b64decode( data[name] )
			self.name = '%X.jpg' % zlib.adler32( photo ) # create unique filename
			self.file = SimpleUploadedFile( self.name, photo, 'image/jpeg' )
			return self.file
		else:
			return None
      