from django import forms

from .models import Logintime

class InputId(forms.ModelForm):
	class Meta:
		model = Logintime
		fields = ['empid']


class AddDetail(forms.ModelForm):
	class Meta:
		model = Logintime
		fields = ['empid', 'intime', 'outtime']