from django.shortcuts import render, redirect, HttpResponse
from .models import *

def edit(request, user_id):
    if request.session['current_user'] == None:
        return redirect('/logout')
    curr_user = User.objects.get(id = user_id)
    context = {
        'curr_user': curr_user
    }
    return render(request, "edit_user/edit_user.html", context)

def update(request, user_id):
    errors = User.objects.validate_edit(request, request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/myaccount/'+user_id)
    if request.session['current_user'] == None:
        return redirect('/logout')
    user = User.objects.get(id = user_id)
    if len(request.POST['first_name']):
        user.first_name = request.POST['first_name']
    if len(request.POST['last_name']):
        user.last_name = request.POST['last_name']
    if len(request.POST['email']):
        user.email = request.POST['email']
    user.save()
    return redirect("/quotes")