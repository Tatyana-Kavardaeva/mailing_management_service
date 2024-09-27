from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from users.views import viewing_users, toggle_activity
from users.apps import UsersConfig
from users.views import UserRegisterView, email_verification, UserPasswordResetView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('password-reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', TemplateView.as_view(template_name='users/password_reset_done.html'),
         name='password-reset-done'),
    path('users/', viewing_users, name='users_list'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity')
]
