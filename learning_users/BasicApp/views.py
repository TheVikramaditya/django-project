from django.shortcuts import render
from . forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect , HttpResponse

# Create your views here.

def index(request):
    return render(request,'BasicApp/home.html')

@login_required
def special(request):
    return HttpResponse("you are logged in")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def signup(request):
    registered =False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
           
            user = user_form.save(commit=False)
            
            user.set_password(user.password)
            
            user.save()
            
            
            profile = profile_form.save(commit=False)
            profile.user = user
            

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            
            
            profile.save()
            registered =True
        else:
            print("error--")
            print(request.FILES['profile_pic'])
            
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'BasicApp/signup.html',{'registered':registered,'user_form':user_form,'profile_form':profile_form})


def user_login(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("A/C not active")
        else:
            print("Someone tried log into your account")
            print("Username:{} and password {}".format(username,password))
            return HttpResponse("Invalid Login Details")
    else:
        return render(request,'BasicApp/login.html')
