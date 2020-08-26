from django import forms
from core.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)

class InterviewForm(forms.Form):

    Title = forms.CharField(max_length=50)
    participant = forms.ModelMultipleChoiceField(queryset=None)
    start = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    end = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M']) 
    
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'

    def __init__(self, *args, **kwargs):
        super(InterviewForm, self).__init__(*args, **kwargs)
        self.fields['participant'].queryset = Participant.objects.all()