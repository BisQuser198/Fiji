from django.shortcuts import render

# docx_replace/views.py
import ast, tempfile
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ReplaceForm
from .utils import batch_find_replace

def replace_view(request):
    if request.method == "POST":
        form = ReplaceForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            # Save uploaded Excel to a temp file
            excel_temp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
            for chunk in cd['excel_file'].chunks():
                excel_temp.write(chunk)
            excel_temp.flush()

            # Read ZIP bytes
            zip_bytes = cd['docx_zip'].read()

            # Parse replacements list
            replacements = ast.literal_eval(cd['replacements'])

            # Run utility
            output_zip, logs = batch_find_replace(
                excel_path=excel_temp.name,
                header_rows=cd['header_rows'],
                id_col_letter=cd['id_col_letter'],
                filename_pattern=cd['filename_pattern'],
                start_id=cd['start_id'],
                end_id=cd['end_id'],
                replacements=replacements,
                docx_zip_bytes=zip_bytes
            )

            # Return a ZIP file response
            response = HttpResponse(output_zip, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="replaced_docs.zip"'
            # Optionally, you can embed logs in headers or render a template
            return response
    else:
        form = ReplaceForm()

    return render(request, "docx_replace/form.html", {"form": form})
