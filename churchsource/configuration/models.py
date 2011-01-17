import decimal

from django.db import models

STYPES = (
  ('dec', 'Decimal'),
  ('int', 'Integer'),
  ('str', 'String'),
  ('tf', 'True/False')
)

class Setting (models.Model):
  skey = models.SlugField('Key', max_length=75, unique=True)
  name = models.CharField('Name/Description', max_length=255)
  stype = models.CharField('Type', max_length=10, choices=STYPES)
  value = models.CharField('Value', max_length=150, blank=True, null=True)
  
  def _value (self):
    return self.get_value()
    
  def get_value (self):
    value = self.value
    
    if value == '':
      value = None
      
    elif self.stype == 'int':
      value = int(value)
      
    elif self.stype == 'dec':
      value = decimal.Decimal(value)
      
    elif self.stype == 'tf':
      if value.lower() == 'false' or value.lower() == 'no' or value == '0':
        value = False
        
      else:
        value = True
        
    return value
    
  class Meta:
    ordering = ('skey', )
    
def get_key (skey, default=None):
  try:
    value = Setting.objects.get(skey=skey).get_value()
    
  except:
    value = None
    
  return value
  