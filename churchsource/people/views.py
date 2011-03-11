import csv
import time
import datetime
import cStringIO as StringIO

from django import http
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import permission_required
from django.template.defaultfilters import slugify

import churchsource.people.models as pmodels
from churchsource.utils.lib import unorm

@csrf_exempt
def jpegcam_admin (request):
  #TODO add require admin user
  f = SimpleUploadedFile(time.strftime("%a%d%b%Y_%H%M%S.jpg"), request.raw_post_data, 'image/jpeg' )
  
  t = pmodels.TempImage(image=f)
  t.save()
  
  return http.HttpResponse('OK:%d:%s: \n\n' % (t.id, t.image.url), mimetype="text/plain")
  
@permission_required('people.add_group')
def reports (request):
  format = request.REQUEST.get('format', '')
  gids = request.REQUEST.getlist('group')
  groups = pmodels.Group.objects.filter(id__in=gids)
  
  if format == 'csv':
    now = datetime.datetime.now()
    output = StringIO.StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(('Last Name', 'First Name', 'E-Mail', 'Gender', 'Birthday', 'Address Type', 'Address', 'Address 2', 'City', 'State', 'Zip', 'Address Notes', 'Phone(s)'))
    for g in groups:
      csv_writer.writerow(('%s Members' % g.name,))
      
      for p in g.person_set.all():
        if p.household.address_set.all().count() == 0:
          csv_writer.writerow((
            unorm(p.lname),
            unorm(p.fname),
            p.email,
            p.get_gender_display(),
            p.birthday(),
            '', '', '', '', '', '', '',
            unorm(p.phone_string())
          ))
          
        else:
          for a in p.household.address_set.all():
            csv_writer.writerow((
              unorm(p.lname),
              unorm(p.fname),
              p.email,
              p.get_gender_display(),
              p.birthday(),
              a.get_atype_display(),
              unorm(a.address1),
              unorm(a.address2),
              unorm(a.city),
              unorm(a.state),
              unorm(a.zipcode),
              unorm(a.notes),
              unorm(p.phone_string())
            ))
            
      csv_writer.writerow((' ',))
      
    response = http.HttpResponse(output.getvalue(), mimetype="text/csv")
    response['Content-Disposition'] = 'attachment; filename=group-report_%d-%d-%d_%d-%d.csv' % (now.year, now.month, now.day, now.hour, now.minute)
    return response
    
  return request.render_to_response('people/group_report.html', {'groups': groups})
  