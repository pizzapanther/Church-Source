from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings

import churchsource.check_in.models as cmodels

class EventForm (forms.Form):
  name = forms.CharField(max_length=255)
  start = forms.TimeField(input_formats=settings.TIME_INPUT_FORMATS, widget=forms.TimeInput(attrs={'class':'tpicker'}))
  end = forms.TimeField(input_formats=settings.TIME_INPUT_FORMATS, required=False, widget=forms.TimeInput(attrs={'class':'tpicker'}))
  
EventFormSet = formset_factory(EventForm, extra=5)
