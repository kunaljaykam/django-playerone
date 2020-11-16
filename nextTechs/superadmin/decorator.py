from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles = []):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

                if group in allowed_roles:
                    return view_function(request, *args, **kwargs)
                else:
                    return redirect('unauth_user')

            return view_function(request, *args, **kwargs)
        return wrapper_function
    return decorator


def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        else:
            return view_function(request, *args, **kwargs)

    return wrapper_function