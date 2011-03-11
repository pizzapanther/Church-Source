import time
import datetime

from django.db import models
from django.conf import settings
import django.contrib.localflavor.us.models as us
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse

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
  ('hw', 'Husband/Wife'),
  ('ds', 'Daughter/Son'),
  ('gparent', 'Grand Parent'),
  ('bs', 'Brother/Sister'),
  ('nn', 'Niece/Nephew'),
  ('au', 'Aunt/Uncle'),
  ('friend', 'Friend'),
  ('other', 'Other')
)

class TempImage (models.Model):
  image = models.ImageField(upload_to=settings.UPLOAD_DIR + "people/tempimage/%Y-%m", blank=True, null=True)
  ts = models.DateTimeField('Time Stamp', auto_now_add=True)
  
  def __unicode__ (self):
    return self.image.name
    
  def view (self):
    return '<img src="%s" alt="" width="100"/>' % self.image.url
    
  view.allow_tags = True
  
  class Meta:
    ordering = ('-ts',)
    
class Household (models.Model):
  name = models.CharField('Household Name', max_length=150)
  status = models.CharField('Marital Status', choices=MSTATUSES, max_length=10, default='ns')
  anniversary = models.DateField('Anniversary', blank=True, null=True)
  active = models.BooleanField('Active', default=True)
  barcode = models.CharField('Check In Barcode', max_length=255, blank=True, null=True)
  notes = models.TextField('Notes', blank=True, null=True)
  first_visit = models.DateField('First Visit', blank=True, null=True)
  image = models.ImageField(upload_to=settings.UPLOAD_DIR + "people/family/%Y-%m", blank=True, null=True)
  image_temp = models.ForeignKey(TempImage, blank=True, null=True)
  
  def checkable (self):
    return self.person_set.filter(groups__gtype__in=['checkinc', 'checkina']).distinct()
    
  def uncheckable (self):
    return self.person_set.exclude(groups__gtype__in=['checkinc', 'checkina']).distinct().order_by('id')
    
  def save (self):
    super(Household, self).save()
    if self.image_temp:
      self.image = SimpleUploadedFile(time.strftime("%a%d%b%Y_%H%M%S.jpg"), self.image_temp.image.read(), 'image/jpeg')
      tid = self.image_temp.id
      self.image_temp = None
      super(Household, self).save()
      
      TempImage.objects.get(id=str(tid)).delete()
      
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
  image_temp = models.ForeignKey('TempImage', blank=True, null=True)
  allergies = models.CharField('Allergies', max_length=255, blank=True, null=True)
  
  groups = models.ManyToManyField('Group', blank=True, null=True)
  
  def phone_string (self):
    ret = u''
    for phone in self.phone_set.all():
      if phone.description():
        ret += phone.description() + ': '
        
      ret += phone.number + ', '
      
    if len(ret) > 0:
      ret = ret[:-2]
      
    return ret
    
  def is_minor (self):
    if self.bdate:
      year18 = datetime.timedelta(days=365*18)
      if year18 > datetime.date.today() - self.bdate:
        return True
        
    return False
    
  def is_adult (self):
    if self.groups.filter(gtype='checkinc').count() == 0:
      return True
      
    else:
      return False
      
  def save (self):
    super(Person, self).save()
    if self.image_temp:
      self.image = SimpleUploadedFile(time.strftime("%a%d%b%Y_%H%M%S.jpg"), self.image_temp.image.read(), 'image/jpeg')
      tid = self.image_temp.id
      self.image_temp = None
      super(Person, self).save()
      
      TempImage.objects.get(id=str(tid)).delete()
      
  def __unicode__ (self):
    if self.mname:
      return '%s, %s %s' % (self.lname, self.fname, self.mname)
      
    else:
      return '%s, %s' % (self.lname, self.fname)
      
  def birthday (self):
    if self.bdate:
      return self.bdate.strftime('%m/%d/%Y')
      
    return ''
    
  def active (self):
    if self.household.active:
      return '<img src="%simg/admin/icon-yes.gif" alt="True">' % settings.ADMIN_MEDIA_PREFIX
      
    return '<img src="%simg/admin/icon-no.gif" alt="False">' % settings.ADMIN_MEDIA_PREFIX
    
  active.allow_tags = True
  
  def edit_household (self):
    return '<a href="../household/%d/">Edit Household</a>' % self.id
    
  edit_household.allow_tags = True
  
  def phones (self):
    ret = '<table>'
    if self.id:
      ret += '<tr><td><strong>Description</strong></td><td><strong>Number</strong></td><td><strong>SMS Alerts On</strong></td></tr>'
      for phone in self.phone_set.all():
        ret += '<tr><td>%s</td><td>%s</td><td style="text-align: center; font-size: 160%%;">%s</td></tr>' % (phone.description(), phone.number, phone.sms_alerts())
        
    ret += '</table>'
    return ret
    
  phones.allow_tags = True
  
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
  state = models.CharField('State', max_length=150)
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
    
  def sms_alerts (self):
    if self.alerts:
      return '&#10003;'
      
    return '-'
    
  def description (self):
    ret = ''
    if self.type1 != 'ns':
      ret += '%s ' % self.get_type1_display()
      
    if self.type2 != 'ns':
      ret += '%s' % self.get_type2_display()
      
    return ret
    
  class Meta:
    ordering = ('person__lname', 'person__fname', 'number')
    
GTYPES = (('general', 'General'), ('checkinc', 'Check In w/ Tag and Code'), ('checkina', 'Check In w/ Tag'))

class Group (models.Model):
  name = models.CharField('Name', max_length=255)
  gtype = models.CharField('Type', max_length=10, choices=GTYPES, default="general")
  desc = models.CharField('Description', max_length=255, blank=True, null=True)
  auth = models.BooleanField('Authorized Volunteer/Staff Group', default=False)
  
  def report (self):
    return 'Report:&nbsp; <a href="%(url)s?group=%(id)d" target="_blank">Print</a> &nbsp;-&nbsp; <a href="%(url)s?group=%(id)d&format=csv">Spreadsheet</a>' % {'url': reverse('cs_group_report'), 'id': self.id}
    
  report.allow_tags = True
  
  def __unicode__ (self):
    return self.name
    
  class Meta:
    ordering = ('name',)
    
class GroupAdmin (models.Model):
  person = models.ForeignKey(Person)
  group = models.ForeignKey(Group)
  can_send = models.BooleanField('Can Send Broadcast Messages', default=True)
  
  def __unicode__ (self):
    return '%s - %s' % (self.group.name, self.person.lname)
    
  class Meta:
    ordering = ('group__name', 'person__lname', 'person__fname')
    