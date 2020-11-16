from django.shortcuts import render
from .models import Employee
from django.contrib.auth.decorators import login_required
from superadmin.decorator import allowed_users
# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def home(request):
    user = Employee.objects.get(user_name_id=request.user)
    context = {
        'user': user,
        'title': 'Employee'
    }
    return render(request, 'employee_home.html', context)