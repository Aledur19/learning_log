from django.urls import path
from django.conf.urls import url
# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from . import views

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('loguout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('user_info/<str:user_username>', views.user_info, name='user_info'),
    path('user_edit/<str:user_username>', views.user_edit, name='user_edit'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password', PasswordResetView.as_view(
        template_name='users/reset_password.html',
        success_url='users:password_reset_done',
        email_template_name='users/reset_password_email.html'
    ), name='reset-password'),
    path('reset-password/done', PasswordResetDoneView.as_view(
    ), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        success_url='users:password_reset_complete'
    ), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(
    ), name='password_reset_complete'),
]