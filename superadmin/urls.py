from django.urls import path
from . import views


urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('superadmin_register', views.register_view, name='superadmin_register'),
    path('unauth_user', views.not_auth_user, name = 'unauth_user'),
    path('download-data', views.add_from_sheet, name='download-data')
]