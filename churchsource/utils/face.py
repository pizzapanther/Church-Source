import re

from django.conf import settings

import churchsource.people.models as pmodels

from face_client import face_client

def find_households (img_url):
  client = face_client.FaceClient(settings.FACE_COM_KEY, settings.FACE_COM_SECRET)
  try:
    response = client.faces_recognize('all', img_url, namespace=settings.FACE_COM_NAMESPACE)
    
  except:
    return None
    
  uids = response['photos'][0]['tags'][0]['uids']
  if len(uids) > 0:
    ret = []
    used = []
    
    for uid in uids:
      uid = uid['uid'].replace('@' + settings.FACE_COM_NAMESPACE, '')
      if re.search("^p", uid):
        uid = uid.replace('p', '')
        try:
          p = pmodels.Person.objects.get(id=uid)
          
        except:
          pass
          
        else:
          #print p
          if p.household.id not in used:
            used.append(p.household.id)
            ret.append(p.household)
            
    return ret
    
  return None
  
