from django.urls import path
from . import views

urlpatterns = [
    # API auth routes
    path('auth/login', views.post_auth_login),
    path('auth/logout', views.post_auth_logout),
    path('auth/student/create', views.post_create_student),
    path('auth/student/update', views.put_edit_student),
    path('auth/user/create', views.post_create_user),
    path('auth/user/update', views.put_edit_user),
    path('auth/user/replace_avatar', views.put_replace_avatar),
    path('auth/get/<str:role>', views.get_user),
    path('auth/get/<int:id>', views.get_user_by_id),
]