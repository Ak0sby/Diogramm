from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('create_report/', views.create_report, name='create_report'),
    path('admin_reports/', views.admin_reports_view, name='admin_reports'),
    path('redirect/', views.login_redirect_view, name='login_redirect'),  # Логинден кийин багыттоо
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Бастапкы логин
]
