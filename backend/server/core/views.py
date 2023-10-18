from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

def auth_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({
            'success': True,
        })
    else:
        return JsonResponse({
            'success': False,
        })
    
def auth_logout(request):
    logout(request)
    return JsonResponse({
        'success': True,
    })