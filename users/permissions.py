from django.shortcuts import redirect
from django.urls import reverse_lazy


class IsLoggedInMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy("users:login_view"))