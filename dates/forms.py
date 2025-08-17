# dates/forms.py
from django import forms

class EarliestDateForm(forms.Form):
    excel_file      = forms.FileField(label="Excel File (.xlsx)")
    skip_rows       = forms.IntegerField(min_value=0, initial=0, label="Header Rows to Skip")
    crit_col_letter = forms.CharField(max_length=3, label="Criteria Column Letter (e.g. B)")
    date_col_letter = forms.CharField(max_length=3, label="Date Column Letter (e.g. D)")
