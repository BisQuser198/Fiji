# investments/forms.py
from django import forms

class InvestmentForm(forms.Form):
    duration = forms.IntegerField(min_value=1, label="Duration (years)")
    initial_balance = forms.FloatField(min_value=0, label="Initial Investment")
    interest_rate = forms.FloatField(label="Base Interest Rate (%)")
    recurring_investment = forms.FloatField(min_value=0, label="Yearly Recurring Investment")

    withdrawals = forms.CharField(
        required=False,
        help_text="e.g. {3: 1000, 5: 500}"
    )
    additional_investments = forms.CharField(
        required=False,
        help_text="e.g. {2: 2000}"
    )
    interest_rate_changes = forms.CharField(
        required=False,
        help_text="e.g. {4: 4.5}"
    )
