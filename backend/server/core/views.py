from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

def auth_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({
            sucess: True,
        })
    else:
        return JsonResponse({
            sucess: False,
        })
