from django.shortcuts import render

# investments/views.py
import base64, ast
from django.shortcuts import render
from .forms import InvestmentForm
from .utils import calculate_interest, plot_yearly_balance

def investment_view(request):
    if request.method == "POST":
        form = InvestmentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Safely parse dict fields or default to {}
            withdrawals = ast.literal_eval(cd["withdrawals"]) if cd["withdrawals"] else {}
            adds = ast.literal_eval(cd["additional_investments"]) if cd["additional_investments"] else {}
            rate_changes = ast.literal_eval(cd["interest_rate_changes"]) if cd["interest_rate_changes"] else {}

            final, profit, invested, balances = calculate_interest(
                duration=cd["duration"],
                initial_balance=cd["initial_balance"],
                interest_rate=cd["interest_rate"],
                withdrawals=withdrawals,
                additional_investments=adds,
                interest_rate_changes=rate_changes,
                recurring_investment=cd["recurring_investment"],
            )

            # Generate the chart
            buf = plot_yearly_balance(balances)
            img_base64 = base64.b64encode(buf.getvalue()).decode("ascii")

            return render(request, "investments/result.html", {
                "final": final,
                "profit": profit,
                "invested": invested,
                "img": img_base64,
                "form": form,
            })
    else:
        form = InvestmentForm()

    return render(request, "investments/form.html", {"form": form})

