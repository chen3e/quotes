from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "login_reg/index.html")

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
            # if the errors object contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/')
    curr_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
    request.session['current_user'] = curr_user.id
    return redirect('/quotes')
    
def login(request):
    curr_user = User.objects.filter(email=request.POST['email'])
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    request.session['current_user'] = curr_user[0].id
    return redirect('/quotes')

def logout(request):
    request.session['current_user'] = None
    return redirect('/')


#for convenience
#def delete(request):
#    User.objects.all().delete()
#    return redirect('/')