from django.shortcuts import render, redirect
import logging, enum

# Create your views here.

# alternative way to add user input fields
class Hard_Coded_Pairs(enum.Enum):
    CLIENT_DATE = "client_date"
    CLIENT_PASSWORD = "client_password"

    def __str__(self):
        return self.name
    
    @classmethod # return iteration of values in Hard_Coded_Pairs
    def values(cls):
        return [option.value for option in Hard_Coded_Pairs]
    
    @classmethod # return iteration of name-value pairs in Hard_Coded_Pairs
    def pairs(cls):
        return [(option.name, option.value) for option in Hard_Coded_Pairs]
# variables values & pairs can be used in CS_game.html to add more input fields
# must add to context

# print(Hard_Coded_Pairs.values()) # OUT: ['client_date', 'client_password']
# print(Hard_Coded_Pairs.pairs()) # OUT: [('CLIENT_DATE', 'client_date'), ('CLIENT_PASSWORD', 'client_password')]

def CS_game_view(request):
    context = {}
    ## List of POST keys
    dict_keys = ["client_text", "client_url", "client_range", "client_email", "client_number"]
    dict_keys.extend(Hard_Coded_Pairs.values())  # add more keys from Hard_Coded_Pairs
    ## append adds as single item, extend adds items 1 by 1 from iterable
    
    ## Populate context with only present, non-empty value
    for key in dict_keys:
        dict_value = request.POST.get(key)
        print("key, dict_value: ", key, dict_value)            # replace print with logger for better control
        if dict_value:
            context[key] = dict_value

## version 4 - loop through context items
    if 1 == 1:
        context = {key: value for key, value in context.items() if value}
        # context = dict ; .items() method returns view object of (key, value) pairs
        # Example: [('brand', 'Ford'), ('model', 'Mustang'), ('year', 1964)]
    client_text = context.get("client_text")
    if client_text:
        context["reversed_text"] = client_text[::-1]

    client_url = context.get("client_url")
    if client_url:
        return redirect(client_url)
    return render(request, "CS_game.html", {"context": context, **context})

## version 3
    client_text = context.get("client_text") # replace if context b/c key might not exist
    if client_text:
        context["reversed_text"] = client_text[::-1]
        return render(request, "CS_game.html", context)
    
    client_url = context.get("client_url")
    if client_url:
        return redirect(client_url)
    return render(request, "CS_game.html", context)

## version 2
    # try:
    #     if context["client_text"]:
    #         # reverse_client_text = context["client_text"][::-1]
    #         # context["reversed_text"] = reverse_client_text
    #         context["reversed_text"] = context["client_text"][::-1]
    #         return render(request, "CS_game.html", context)
    # except KeyError as e:
    #     logging.warning(f"KeyError: {e} - 'client_text' not found in context.")

    # try:
    #     if context["client_url"]:
    #         target_url = context["client_url"]
    #         # if user inputs url, then redirect to that url            
    #         return redirect(target_url)
    # except KeyError as e:
    #     logging.warning(f"KeyError: {e} - 'client_url' not found in context.")

    # return render(request, "CS_game.html", context)

## version 1
# def CS_game_view(request):
#     context = {}
#     client_text = request.POST.get("client_text")
#     print("Client Text:", client_text)  # Debugging line to check the value
#     if client_text:
#         context["client_text"] = client_text
    
#     client_url = request.POST.get("client_url")
#     print("Client URL:", client_url)  # Debugging line to check the value
#     if client_url:
#         context["client_url"] = client_url

#     client_range = request.POST.get("client_range")
#     print("Client Range:", client_range)  # Debugging line to check the value
#     if client_range:
#         context["client_range"] = client_range

#     client_email = request.POST.get("client_email")
#     print("Client Email:", client_email)  # Debugging line to check the value
#     if client_email:
#         context["client_email"] = client_email

#     client_number = request.POST.get("client_number")
#     print("Client Number:", client_number)  # Debugging line to check the value
#     if client_number:
#         context["client_number"] = client_number
    

#     return render(request, "CS_game.html", context)

from django.shortcuts import render, redirect
from .models import Employee
from .forms  import EmployeeForm

def CS_game_view2(request):
    # Handle form submissions for add / update / delete
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            form = EmployeeForm(request.POST) # instantiate object EmployeeForm with POST data
            if form.is_valid():
                form.save()             # INSERT into employee table of db.sqlite3
                return redirect(request.path)

        elif action == 'update':
            emp = Employee.objects.get(pk=request.POST['id'])
            form = EmployeeForm(request.POST, instance=emp)
            if form.is_valid():
                form.save()             # UPDATE employee row
                return redirect(request.path)

        elif action == 'delete':
            Employee.objects.get(pk=request.POST['id']).delete()
            return redirect(request.path)

    # On GET (or after redirect), show the list and an empty form
    employees = Employee.objects.all().order_by('id') # query DB for all rows
    # Employee.objects.all() runs SELECT 
    form      = EmployeeForm()         # blank form for “create”
    return render(request, 'CS_game2.html', {
        'employees': employees,
        'form': form,
    })


import matplotlib.pyplot as plt      # plotting library
import io                             # in-memory byte buffer
import base64                         # encode image for embedding

def CS_game_view3(request):
# Read client_number from POST, compute f(x)=x**2+1, create a PNG plot, pass data-URL to template

    context = {}        # collect context values for template
    img_data_url = None   # will hold data URL if we generate a plot

    if request.method == "POST":
        # get value from form (string) and try to convert to float
        process_number = request.POST.get("client_number")

        if process_number:
            try:
                x = int(process_number)          # convert input to number
                context["client_number"] = x
                context["function_result"] = x**2 + 1   # f(x)=x**2+1

                # define the axes for the plot
                xs = list(range(int(x+1)))  
                ys = [xi**2 + 1 for xi in xs]                 # f(x)=x**2+1
                # create plot (figure)
                fig, ax = plt.subplots(figsize=(6, 3.5))     # creates figure object and one plot area
                # fig = plt.figure(figsize=(6, 3.5)) -- container for 1+ axes
                # ax = fig.add_subplot(1, 1, 1)        # 1 row, 1 col, subplot index 1
                ax.plot(xs, ys, color="tab:blue")             # line
                ax.axvline(x, color="green", linestyle="--")   # vertical line at input x
                ax.scatter([x], [x**2 + 1], color="green")     # highlight point
                ax.set_title(f"f(x)=x^2+1 for x in range of 1 to x={x}")     # title
                ax.set_xlabel("x")
                ax.set_ylabel("f(x)")

                # save figure to in-memory buffer as PNG
                buffer = io.BytesIO() # MEMORIZE: make an in-memory bynary steam you can write/read from
                fig.tight_layout()
                fig.savefig(buffer, format="png") # render & write PNG bytes into buffer
                plt.close(fig)               # close figure to free memory
                buffer.seek(0) # move buffer cursor to beginning (so we can read from start)

                # # encode PNG to base64 for embedding in HTML
                # img_b64 = base64.b64encode(buffer.read()).decode("ascii")
                # img_data_url = f"data:image/png;base64,{img_b64}"
                # # step by step version
                raw_bytes = buffer.read()
                img_b64_bytes = base64.b64encode(raw_bytes) # encode raw bytes into a bytes obj using base64 module
                img_b64 = img_b64_bytes.decode("ascii") # convert bytes obt into string (to concatenate into adata URL to embed in HTML)
                img_data_url = f"data:image/png;base64,{img_b64}"


            except ValueError:
                context["error"] = "Invalid number"

    return render(request, "CS_game3.html", {"context": context, "plot_data_url": img_data_url})