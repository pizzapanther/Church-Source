import time

from django import http
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import permission_required

import churchsource.people.models as pmodels

@csrf_exempt
def jpegcam_admin (request):
  #TODO add require admin user
  f = SimpleUploadedFile(time.strftime("%a%d%b%Y_%H%M%S.jpg"), request.raw_post_data, 'image/jpeg' )
  
  t = pmodels.TempImage(image=f)
  t.save()
  
  return http.HttpResponse('OK:%d:%s: \n\n' % (t.id, t.image.url), mimetype="text/plain")
  
@permission_required('people.add_group')
def reports (request):
  gids = request.REQUEST.getlist('group')
  groups = pmodels.Group.objects.filter(id__in=gids)
  
  return request.render_to_response('people/group_report.html', {'groups': groups})
  