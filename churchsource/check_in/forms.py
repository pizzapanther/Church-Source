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
    widgets = {
      'alerts': cwidgets.TouchBox(attrs={'tvalue': 'ON', 'label': 'Receive E-Mail Alerts'}),
      'image_temp': forms.HiddenInput,
    }