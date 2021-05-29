from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
 
app_name = "usermanager"

urlpatterns = [  
    path('login/', views.login,name="login"), 
    path('logout/',views.Logout,name='logout'),
   
]