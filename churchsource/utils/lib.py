import unicodedata

def unorm (ustring):
  ret = ''
  if ustring:
    ret = unicodedata.normalize('NFKD', ustring).encode('ascii','ignore')
    
  return ret
  