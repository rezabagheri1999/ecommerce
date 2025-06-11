from pyexpat.errors import messages
from django.contrib.auth import login,get_user_model,logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def header_sec(request):
    context = {

    }
    return render(request,'base/Header.html' ,context)

def footer_sec(request):
    context = {

    }
    return render(request , 'base/Footer.html',context)


def home_page(request):
    context = {

    }
    return render(request,'home_page.html',context)


