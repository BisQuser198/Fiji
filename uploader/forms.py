from django import forms

class UploadForm(forms.Form):
    file = forms.FileField(label='Select a file')
# forms.FileField creates an HTML <input type="file"> element
# forms.FileField wraps the file content in an UploadedFile object when the form is submitted