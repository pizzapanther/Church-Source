from django.db import models
from django.conf import settings
import django.contrib.localflavor.us.models as us

MSTATUSES = (
  ('ns', 'Not Specified'),
  ('single', 'Single'),
  ('married', 'Married'),
  ('divorced', 'Divorced'),
  ('other', 'Other')
)

GENDERS = (
  ('ns', 'Not Specified'),
  ('male', 'Male'),
  ('female', 'Female')
)

FAMILY_ROLES = (
  ('ns', 'Not Specified'),
  ('single', 'Single'),
  ('wife', 'Wife'),
  ('husband', 'Husband'),
  ('daughter', 'Daughter'),
  ('son', 'Son'),
  ('gparent', 'Grand Parent'),
  ('bs', 'Brother/Sister'),
  ('nn', 'Niece/Nephew'),
  ('au', 'Aunt/Uncle'),
  ('friend', 'Friend'),
  ('otherr', 'Other Relation'),
  ('pet', 'Pet'),
  ('other', 'Other')
)

class Household (models.Model):
  name = models.CharField('Household Name', max_length=150)
  status = models.CharField('Marital Status', choices=MSTATUSES, max_length=10, default='ns')
  anniversary = models.DateField('Anniversary', blank=True, null=True)
  active = models.BooleanField('Active', default=True)
  barcode = models.CharField('Check In Barcode', max_length=255, blank=True, null=True)
  notes = models.TextField('Notes', blank=True, null=True)
  first_visit = models.DateField('First Visit', blank=True, null=True)
  image = models.ImageField(upload_to=settings.UPLOAD_DIR + "people/family/%Y-%m", blank=True, null=True)
  
  def __unicode__ (self):
    return self.name
    
  def anniversary_ (self):
    return self.anniversary.strftime('%m/%d/%Y')
    
  def members (self):
    ret = ''
    for p in self.person_set.all():
      if p.lname == self.name:
        ret += '%s, ' % p.fname
        
      else:
        ret += '%s %s, ' % (p.fname, p.lname)
        
    return ret[:-2]
    
  class Meta:
    ordering = ('name', )
    
class Person (models.Model):
  household = models.ForeignKey(Household)
  
  fname = models.CharField('First Name', max_length=150)
  mname = models.CharField('Middle Name', max_length=150, blank=True, null=True)
  lname = models.CharField('Last Name', max_length=150)
  email = models.EmailField('E-Mail', blank=True, null=True)
  alerts = models.BooleanField('Receive E-Mail Alerts', default=True)
  gender = models.CharField('Gender', choices=GENDERS, max_length=10, default='ns')
  role = models.CharField('Role', choices=FAMILY_ROLES, max_length=10, default='ns')
  bdate = models.DateField('Birth Date', blank=True, null=True)
  ddate = models.DateField('Deceased', blank=True, null=True)
  image = models.ImageField(upload_to=settings.UPLOAD_DIR + "people/person/%Y-%m", blank=True, null=True)
  allergies = models.CharField('Allergies', max_length=255, blank=True, null=True)
  
  def __unicode__ (self):
    return '%s %s' % (self.fname, self.lname)
    
  def birthday (self):
    return self.bdate.strftime('%m/%d/%Y')
    
  def active (self):
    if self.household.active:
      return '<img src="%simg/admin/icon-yes.gif" alt="True">' % settings.ADMIN_MEDIA_PREFIX
      
    return '<img src="%simg/admin/icon-no.gif" alt="False">' % settings.ADMIN_MEDIA_PREFIX
    
  active.allow_tags = True
  
  def edit_household (self):
    return '<a href="../household/%d/">Edit Household</a>' % self.id
    
  edit_household.allow_tags = True
  
  def details (self):
    if self.id:
      return '<a href="../../person/%d/">Edit Details</a>' % self.id
      
    return ''
    
  details.allow_tags = True
    
  class Meta:
    verbose_name_plural = "People"
    ordering = ('lname', 'fname')
    
ATYPES = (
  ('ns', 'Not Specified'),
  ('home', 'Home'),
  ('school', 'College'),
  ('vacation', 'Vacation'),
  ('other', 'Other'),
)

class Address (models.Model):
  household = models.ForeignKey(Household)
  
  address1 = models.CharField('Address 1', max_length=255)
  address2 = models.CharField('Address 2', max_length=255, blank=True, null=True)
  city = models.CharField('City', max_length=255)
  state = us.USStateField()
  zipcode = models.CharField('Zip Code', max_length=25)
  atype = models.CharField('Type', max_length=10, choices=ATYPES, default='ns')
  notes = models.CharField('Notes', max_length=255, blank=True, null=True, help_text="If the address is for one particular family member, list their names here.")
  
  def __unicode__ (self):
    return "%s: %s" % (self.get_atype_display(), self.address1)
    
  class Meta:
    ordering = ('address1',)
    
PTYPES1 = (('ns', 'Not Specified'), ('home', 'Home'), ('personal', 'Personal'), ('work', 'Work'))
PTYPES2 = (('ns', 'Not Specified'), ('pager', 'Pager'), ('mobile', 'Mobile'), ('fax', 'Fax'), ('phone', 'Phone'))

class Phone (models.Model):
  person = models.ForeignKey(Person)
  
  number = us.PhoneNumberField()
  type1 = models.CharField('Type 1', max_length=10, choices=PTYPES1, default="ns")
  type2 = models.CharField('Type 2', max_length=10, choices=PTYPES2, default="ns")
  alerts = models.BooleanField('Use for SMS alerts', default=False)
  
  def __unicode__ (self):
    ret = self.description()
    if ret == '':
      return self.number
      
    return ret
    
  def description (self):
    ret = ''
    if self.type1 != 'ns':
      ret += '%s ' % self.get_type1_display()
      
    if self.type2 != 'ns':
      ret += '%s' % self.get_type2_display()
      
    return ret
    
  class Meta:
    ordering = ('person__lname', 'person__fname', 'number')
    