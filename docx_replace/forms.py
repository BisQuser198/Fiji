# docx_replace/forms.py
from django import forms

# We’ll parse replacements via ast.literal_eval in the view.
class ReplaceForm(forms.Form):
    excel_file = forms.FileField(label="Upload Source EXCEL (.xlsx)", help_text='Example: Laying and connection of LV AC Cables 14Jul2025.xlsx')
    docx_zip   = forms.FileField(label="Upload DOCX Target Files ZIP archive", help_text='Example: cloned_files(3).zip')

    header_rows     = forms.IntegerField(min_value=0, initial=0, label="Header rows to skip", help_text='Top rows to ignore in Excel file')
    id_col_letter   = forms.CharField(max_length=2, initial="A", label="ID column (e.g. G)", help_text='Column you use to match ID from Excel to ID from Word')
    filename_pattern = forms.CharField(
        label="Input pattern of DOCX filename + {id}",
        help_text="Use {id} placeholder, e.g. '6 Proces Verbal Lucrare Calitativa Impamantare TS{id}.docx'"
    )
    start_id        = forms.IntegerField(label="Starting number for {id}")
    end_id          = forms.IntegerField(label="Ending number for {id}",
                                         help_text = "Explanation: this is the range of files which you will edit")

    replacements = forms.CharField(
        widget=forms.Textarea,
        label="Replace rules",
        help_text="\nThis is a list of words/phrases that you will replace - Use format JSON list of ['find_text', 'col_letter'], e.g. [[\"name\",\"B\"],[\"date\",\"C\"]]"
    )
    
