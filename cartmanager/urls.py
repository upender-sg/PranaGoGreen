
from django.contrib import admin
from django.urls import path, include
from usermanager import views as userviews
from . import views as pranaviews

urlpatterns = [
     path('',  pranaviews.home ),
   

]
