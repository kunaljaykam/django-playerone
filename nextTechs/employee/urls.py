from django.urls import path
from . import views


urlpatterns = [
    path('employee-home', views.home, name='employee-home'),

]