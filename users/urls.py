
from django.urls import path
from .views import LoginView,UserCreateView,Dashboard,logout_user

app_name="users"


urlpatterns = [

    path("", Dashboard.as_view(), name="dashboard"),
    path("login/", LoginView.as_view(), name="login_view"),
    path("logout/", logout_user, name="logout"),

    path("register/", UserCreateView.as_view(), name="register_view"),
    
]

