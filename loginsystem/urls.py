from django.urls import path
from .views import index, logout,register,login
urlpatterns = [
    path('member',index,name="member"),
    path('register/add',register,name="addUser"),
    path('login',login,name="login"),
    path('logout',logout,name="logout"),
]
