
from django.urls import path
from .views import LoginView,UserRegisterView,Dashboard,logout_user,UserCreateView,UserUpdateView,UserListView,UserDeleteView

app_name="users"


urlpatterns = [

    path("", Dashboard.as_view(), name="dashboard"),
    path("login/", LoginView.as_view(), name="login_view"),
    path("logout/", logout_user, name="logout"),
    path("register/", UserRegisterView.as_view(), name="register_view"),
    path("user/", UserListView.as_view(), name="user_view"),
    path("user/create", UserCreateView.as_view(), name="user_create_view"),

    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user_update_view"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete_view"),

    
]

