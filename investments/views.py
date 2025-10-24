from django.shortcuts import render

# investments/views.py
import base64, ast
from django.shortcuts import render
from .forms import InvestmentForm
from .utils import calculate_interest, plot_yearly_balance

def investment_view(request):
    if request.method == "POST":
        form = InvestmentForm(request.POST)
        if form.is_valid(): # runs field validators / checks each input and clean(), return True/False; populates form.cleaned_data; populates form_errors if validation fails
            cd = form.cleaned_data # cleaned_data is a dict of validated data from user input

            # Safely parse dict fields or default to {}
            withdrawals = ast.literal_eval(cd["withdrawals"]) if cd["withdrawals"] else {}
            # cd["withdrawals"] -> access value of withdrawls field
            # ast.literal_eval() passes a sring into the data type (here, a dict)
            # ast.literal_eval() - F. from Python ast (abstract syntax tree) module
            # can also use eval() - evaluate expression & donvert data from one format to another
            # eval() evaluates expressions passed as a string - syntax: eval(expression)
            # exp = "2 + 3" ; res = eval(exp) ; print(res) # OUT 5
            #ast_literal_eval() evalutes a string containing a Pyton literal or a container / object
            # s = "[1, 2, 3, 4]" ; res = ast.literal_eval(s) ; print(res) ; OUT: [1, 2, 3, 4] -- returns a list
            adds = ast.literal_eval(cd["additional_investments"]) if cd["additional_investments"] else {}
            rate_changes = ast.literal_eval(cd["interest_rate_changes"]) if cd["interest_rate_changes"] else {}

            # calculate_interest => calculates balances
            final, profit, invested, balances = calculate_interest(
                duration=cd["duration"],
                initial_balance=cd["initial_balance"],
                interest_rate=cd["interest_rate"],
                withdrawals=withdrawals,
                additional_investments=adds,
                interest_rate_changes=rate_changes,
                recurring_investment=cd["recurring_investment"],
            )

            # Generate the chart - balances from calculate_interest is passed
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

