from django import forms
from django.forms.formsets import formset_factory

import churchsource.check_in.models as cmodels

class EventForm (forms.Form):
  name = forms.CharField(max_length=255)
  start = forms.TimeField(widget=forms.TextInput(attrs={'class':'tpicker'}))
  end = forms.TimeField(required=False, widget=forms.TextInput(attrs={'class':'tpicker'}))
  
EventFormSet = formset_factory(EventForm, extra=5)
