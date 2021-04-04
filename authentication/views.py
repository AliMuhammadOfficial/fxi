from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from accounts.models import AccountUser


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.user.is_authenticated:
        return redirect('/dashboard')
    elif request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/dashboard")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    
    return render(
        request,
        "accounts/login.html",
        {
        "form": form,
        "msg" : msg
        }
    )

def register_user(request):

    msg     = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            account_user = AccountUser.objects.create(user=user)
            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            return redirect("/login/")
        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()
    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
            "msg" : msg,
            "success" : success 
        }
    )


def register_user_invited(request, uid):
    msg     = None
    success = False
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg = 'User created - please <a href="/login">login</a>.'
            success = True
            print("UID : ",  uid)
            refferal_exist = AccountUser.objects.filter(uid=uid).exists()
            if refferal_exist:
                try:
                    account_user = AccountUser(user=user, ref_by=uid)
                    account_user.save()
                except Exception as e:
                    print("Exception in Refferal Exist", e)
                    msg += e
            else:
                account_user = AccountUser(user=user)
                account_user.save()
                msg = f"User with {uid} is invalid user."
            return redirect("/login/")
        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()
    return render(
        request,
        "accounts/register.html",
        {
        "form": form,
        "msg" : msg,
        "success" : success 
        }
    )