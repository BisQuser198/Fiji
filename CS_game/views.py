from django.shortcuts import render, redirect
import logging

# Create your views here.


## version 2
def CS_game_view(request):
    context = {}
    ## List of POST keys
    dict_keys = ["client_text", "client_url", "client_range", "client_email", "client_number"]

    ## Populate context with only present, non-empty value
    for key in dict_keys:
        dict_value = request.POST.get(key)
        print("key, dict_value: ", key, dict_value)            # replace print with logger for better control
        if dict_value:
            context[key] = dict_value

    try:
        if context["client_text"]:
            # reverse_client_text = context["client_text"][::-1]
            # context["reversed_text"] = reverse_client_text
            context["reversed_text"] = context["client_text"][::-1]
            return render(request, "CS_game.html", context)
    except KeyError as e:
        logging.warning(f"KeyError: {e} - 'client_text' not found in context.")

    try:
        if context["client_url"]:
            target_url = context["client_url"]
            # if user inputs url, then redirect to that url            
            return redirect(target_url)
    except KeyError as e:
        logging.warning(f"KeyError: {e} - 'client_url' not found in context.")

    return render(request, "CS_game.html", context)

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