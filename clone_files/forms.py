# docxcloner/forms.py
from django import forms

class CloneDocxForm(forms.Form):
    source_file = forms.FileField(label="Upload Source DOCX")
    target_start = forms.IntegerField(label="Starting Target Number", initial=2)
    target_end = forms.IntegerField(label="Ending Target Number", initial=26)
