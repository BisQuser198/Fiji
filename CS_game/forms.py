from django import forms
from .models import Employee

# form to create/update Employee instances --> 3) views.py
class EmployeeForm(forms.ModelForm):
    class Meta:
        model  = Employee
        fields = ['name', 'department_id', 'manager_id', 'salary', 'promotable']
