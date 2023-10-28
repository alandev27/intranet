from django.contrib.auth import authenticate, login, logout
from .lib.fs import format_file, delete_file
from .models import *
from .lib.error import *
from django.core.files.uploadedfile import UploadedFile
from django.http import JsonResponse, HttpRequest, HttpResponse

def post_auth_login(request: HttpRequest) -> HttpResponse:
    if not request.method == 'POST' or request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_INVALID_REQUEST'],
        })
    
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
            'username': username,
            'password': password,
            'success': False,
            'code': errors['ERR_USER_NOT_FOUND'],
        })
    
def post_auth_logout(request: HttpRequest) -> HttpResponse:
    if not request.method == 'POST' or not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_INVALID_REQUEST'],
        })
    logout(request)
    return JsonResponse({
        'success': True,
    })

def post_create_student(request: HttpRequest) -> HttpResponse:
    if not request.method == 'POST':
        return JsonResponse({
            'success': False,
            'code': errors['ERR_INVALID_REQUEST'],
        })
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_NOT_AUTHENTICATED'],
        })
    if request.user.role != 'AD':
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_STATUS_INSUFFICIENT'],
        })
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    avatar = request.FILES.get('avatar')
    current_grade = request.POST.get('current_grade')
    guardian_id = request.POST.get('guardian')
    guardian = Parent.objects.get(pk=guardian_id)

    if not guardian:
        return JsonResponse({
            'success': False,
            'code': errors['WARN_USER_LACKING_GUARDIAN'],
        })

    avatar = format_file(avatar, 'assets/avatars')

    user = Student.objects.create_user(username=username, password=password, phone=phone, address=address, avatar=avatar, current_grade=current_grade, guardian=guardian)

    if user is not None:
        user.save()
        return JsonResponse({
            'success': True,
        })
    else:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_NOT_FOUND'],
        })
    
def put_edit_student(request: HttpRequest) -> HttpResponse:
    if not request.method == 'POST':
        return JsonResponse({
            'success': False,
            'code': errors['ERR_INVALID_REQUEST'],
        })
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_NOT_AUTHENTICATED'],
        })
    
    user = request.user
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    avatar = request.FILES.get('avatar')

    if phone is not None:
        user.phone = phone

    if address is not None:
        user.address = address

    if avatar is not None:
        delete_file(user.avatar.path)
        avatar = format_file(avatar, f'assets/avatars')
        user.avatar = avatar

    user.save()
    
    return JsonResponse({
        'success': True,
    })

def post_create_user(request: HttpRequest) -> HttpResponse:
    if not request.method == 'POST':
        return JsonResponse({
            'success': False,
            'code': errors['ERR_INVALID_REQUEST'],
        })
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_NOT_AUTHENTICATED'],
        })
    if request.user.role != 'AD':
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_STATUS_INSUFFICIENT'],
        })
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    avatar = request.FILES.get('avatar')
    role = request.POST.get('role')

    if role not in UserRole.values:
        return JsonResponse({
            'success': False,
            'code': errors['WARN_INVALID_ROLE'],
        })

    avatar = format_file(avatar, f'assets/avatars')

    user = None

    if role == 'PA':
        user = Parent.objects.create_user(username=username, password=password, phone=phone, address=address, avatar=avatar, role=role)
    elif role == 'TE':
        user = Teacher.objects.create_user(username=username, password=password, phone=phone, address=address, avatar=avatar, role=role)
    elif role == 'AD':
        user = User.objects.create_user(username=username, password=password, phone=phone, address=address, avatar=avatar, role=role)

    if user is not None:
        user.save()
        return JsonResponse({
            'success': True,
        })
    else:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_NOT_FOUND'],
        })
    
def put_edit_user(request: HttpRequest) -> HttpResponse:
    if not request.method == 'POST':
        return JsonResponse({
            'success': False,
            'code': errors['ERR_INVALID_REQUEST'],
        })
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_NOT_AUTHENTICATED'],
        })
    
    user = request.user
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    avatar = request.FILES.get('avatar')

    if phone is not None:
        user.phone = phone

    if address is not None:
        user.address = address

    if avatar is not None:
        delete_file(user.avatar.path)
        avatar = format_file(avatar, f'assets/avatars')
        user.avatar = avatar

    user.save()
    
    return JsonResponse({
        'success': True,
    })

def get_user(request: HttpRequest, role: str) -> HttpResponse:
    if not request.method == 'GET':
        return JsonResponse({
            'success': False,
            'code': errors['ERR_INVALID_REQUEST'],
        })
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_NOT_AUTHENTICATED'],
        })
    
    user = request.user

    if role not in UserRole.values:
        return JsonResponse({
            'success': False,
            'code': errors['WARN_INVALID_ROLE'],
        })

    if role == 'PA':
        user = Parent.objects.get(pk=user.pk)
    elif role == 'TE':
        user = Teacher.objects.get(pk=user.pk)
    elif role == 'AD':
        user = User.objects.get(pk=user.pk)

    if user is not None:
        return JsonResponse({
            'success': True,
            'user': user,
        })
    else:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_NOT_FOUND'],
        })

def get_user_by_id(request: HttpRequest, id: int) -> HttpResponse:
    if not request.method == 'GET':
        return JsonResponse({
            'success': False,
            'code': errors['ERR_INVALID_REQUEST'],
        })
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_NOT_AUTHENTICATED'],
        })
    user_role = request.user.role

    if user_role not in UserRole.values:
        return JsonResponse({
            'success': False,
            'code': errors['WARN_INVALID_ROLE'],
        })
    
    user = request.user

    if user_role == 'PA':
        user = Parent.objects.get(pk=user.pk)
    elif user_role == 'TE':
        user = Teacher.objects.get(pk=user.pk)
    elif user_role == 'AD':
        user = User.objects.get(pk=user.pk)

    if user is not None:
        return JsonResponse({
            'success': True,
            'user': user,
        })
    else:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_NOT_FOUND'],
        })

def put_replace_avatar(request: HttpRequest) -> HttpResponse:
    if not request.method == 'POST':
        return JsonResponse({
            'success': False,
            'code': errors['ERR_INVALID_REQUEST'],
        })
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'code': errors['ERR_USER_NOT_AUTHENTICATED'],
        })
    
    user_id = request.POST.get('user_id')
    user_role = request.POST.get('role')

    if user_role not in UserRole.values:
        return JsonResponse({
            'success': False,
            'code': errors['WARN_INVALID_ROLE'],
        })

    user = None

    if user_role == 'PA':
        user = Parent.objects.get(pk=user_id)
    elif user_role == 'TE':
        user = Teacher.objects.get(pk=user_id)
    elif user_role == 'ST':
        user = Student.objects.get(pk=user_id)
    elif user_role == 'AD':
        user = User.objects.get(pk=user_id)

    avatar = request.FILES.get('avatar')
    delete_file(user.avatar.path)
    avatar = format_file(avatar, f'assets/avatars')
    user.avatar = avatar
    user.save()

    return JsonResponse({
        'success': True,
    })
