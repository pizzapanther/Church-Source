from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings

import churchsource.check_in.models as cmodels
import churchsource.people.models as pmodels
import churchsource.check_in.widgets as cwidgets

class PersonForm (forms.ModelForm):
  class Meta:
    model = pmodels.Person
    fields = ('fname', 'lname', 'gender', 'role', 'bdate', 'allergies', 'image_temp', 'groups')
    widgets = {'image_temp': forms.HiddenInput, 'bdate': forms.DateInput(format='%m/%d/%Y')}
    
class HouseholdForm (forms.ModelForm):
  class Meta:
    model = model = pmodels.Household
    fields = ('name', 'barcode', 'image_temp')
    
    widgets = {
      'image_temp': forms.HiddenInput,
    }
    