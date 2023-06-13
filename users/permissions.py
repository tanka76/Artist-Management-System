from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse_lazy


class IsLoggedInMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy("users:login_view"))
    

def is_logged_in(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect(reverse_lazy("users:login_view"))
    return wrapped_view