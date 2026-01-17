from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request,user)
            messages.success(request,"Logged in Successfully")
            return redirect("list_expenses")
        else:
            messages.error(request,"Invalid Username or Password")
            
        
    return render(request,"accounts/login.html" )


def register_view(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        messages.success(request,"Account Created Successfully. Please Login")

        return redirect('login')
    
    return render(request,"accounts/register.html")

def logout_view(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect("login")
