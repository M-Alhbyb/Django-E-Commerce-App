from base.models import User
from base.profiles import EmployeeProfile
from django import forms

class CreateEmployeeForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'photo']


class CreateEmployeeProfile(forms.ModelForm):
  class Meta:
    model = EmployeeProfile
    fields = ['phone_number', 'address', 'salary']