# file_renamer/forms.py

from django import forms

class RenameForm(forms.Form):
    # Form for user input: zip upload and renaming rules.
    # What it does: Defines fields for the form, with help texts for UX clarity.
    # How it does it: Uses Django's Form class to create labeled fields with validation.
    
    mode = forms.ChoiceField(
        choices=[('basic', 'Basic'), ('custom', 'Custom')],
        initial='basic',
        label='Renaming Mode',
        help_text='Basic: Use a single root label with optional numeric prefix/suffix. Custom: Define multiple groups with text and ranges.'
    )
    zip_file = forms.FileField(
        label='Upload Zip File',
        help_text='Zip containing files to rename (flat structure, no subdirs).'
    )
    root_label = forms.CharField(
        max_length=100,
        required=False,
        label='Root Label',
        help_text='Main text for file names in basic mode (e.g., "file").'
    )
    use_prefix = forms.BooleanField(
        required=False,
        label='Use Numeric Prefix',
        help_text='Add number before root (e.g., 1file).'
    )
    use_suffix = forms.BooleanField(
        required=False,
        label='Use Numeric Suffix',
        help_text='Add number after root (e.g., file1).'
    )
    start_num = forms.IntegerField(
        min_value=1,
        initial=1,
        required=False,
        label='Start Number',
        help_text='Starting number for range (default: 1).'
    )
    end_num = forms.IntegerField(
        min_value=1,
        required=False,
        label='End Number',
        help_text='Ending number (optional; if blank, auto-calculated from file count).'
    )
    custom_rule = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False,
        label='Custom Rules',
        help_text='One group per line: text,start,end (e.g., RTG,1,6<br>TS,1,26). Names will be text + number + original ext.'
    )

    def clean(self):
        # Custom validation for form logic.
        # What it does: Ensures required fields based on mode.
        # How it does it: Checks mode and adds errors if conditions not met.
        cleaned_data = super().clean()
        mode = cleaned_data.get('mode')
        if mode == 'basic':
            if not cleaned_data.get('root_label'):
                self.add_error('root_label', 'Required in basic mode.')
            if not cleaned_data.get('use_prefix') and not cleaned_data.get('use_suffix'):
                self.add_error('use_prefix', 'Select at least one in basic mode.')
                self.add_error('use_suffix', '')
        elif mode == 'custom':
            if not cleaned_data.get('custom_rule'):
                self.add_error('custom_rule', 'Required in custom mode.')
        return cleaned_data