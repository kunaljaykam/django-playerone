from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from .decorator import allowed_users, unauthenticated_user
from employee.models import Employee
from utils.sheets import getEmployeeFromSheets


@login_required(login_url='login')
def home(request):
    group = request.user.groups.all()[0].name
    if group == 'employee':
        return redirect('employee-home')
    else:
        return redirect('superadmin_register')


@unauthenticated_user
def login_view(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password not right')

    return render(request, 'superadmin/login.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['super_admin'])
def register_view(request):
    form = UserRegisterForm()
    groups = Group.objects.all()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = form.cleaned_data.get('username')
            city = request.POST.get('city')
            eid = request.POST.get('eid')
            messages.success(request, f'{user} added')

            user_group = request.POST.get('group_name')

            if user_group == 'employee':
                temp_user = User.objects.get(username=user)
                new_service_temp = Employee(user_name=temp_user, city=city, employee_id=eid)
                new_service_temp.save()

            group = Group.objects.get(name=user_group)
            new_user.groups.add(group)
            return redirect('superadmin_register')

    context = {
        'form': form,
        'groups': groups
    }
    return render(request, 'superadmin/superadmin_register.html', context)


def not_auth_user(request):
    return render(request, 'superadmin/not_auth.html', {})


@login_required(login_url='login')
@allowed_users(allowed_roles=['super_admin'])
def add_from_sheet(request):
    emp_values = getEmployeeFromSheets()
    employee_group = Group.objects.get(name='employee')
    user_added = False
    for employee_values in emp_values:
        user_name = employee_values[0] + employee_values[1] + employee_values[2]
        password = employee_values[0] + employee_values[1] + employee_values[2]
        first_name = employee_values[0]
        last_name = employee_values[1]
        city = employee_values[3]
        eid = employee_values[2]
        if not Employee.objects.filter(employee_id=eid).exists():
            user = User.objects.create_user(username=user_name, first_name=first_name,
                                            last_name=last_name,
                                            password=password)
            user.save()
            user = User.objects.get(username=user_name)
            new_employee = Employee(user_name=user, city=city, employee_id=eid)
            new_employee.save()
            user_added = True

    if user_added:
        messages.info(request, 'user added from sheet')
    else:
        messages.info(request, 'username already present')
    return redirect('home')
