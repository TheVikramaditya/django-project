
from django.urls import path,include
from BasicApp import views

#TEMPLATE TAGGING app_name is global and django will look for it
app_name = 'BasicApp'

urlpatterns = [
   
    path('signup/',views.signup,name="register"),
    path('login/',views.user_login,name="login"),
    
]