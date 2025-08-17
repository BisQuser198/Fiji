from django.shortcuts import render

# Create your views here.
# dates/views.py
from django.shortcuts import render
from django.contrib import messages
from .forms import EarliestDateForm
from .utils import extract_earliest_dates

def earliest_dates_view(request):
    result = None
    if request.method == "POST":
        form = EarliestDateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_bytes = request.FILES['excel_file'].read()
                result = extract_earliest_dates(
                    excel_bytes,
                    form.cleaned_data['skip_rows'],
                    form.cleaned_data['crit_col_letter'],
                    form.cleaned_data['date_col_letter']
                )
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = EarliestDateForm()

    return render(request, "dates/form.html", {
        "form": form,
        "result": result
    })
