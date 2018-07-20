from django.shortcuts import render, redirect
from .models import *

def main(request):
    if request.session['current_user'] == None:
        return redirect('/logout')
    curr_user = User.objects.get(id=request.session['current_user'])
    quotes = Quote.objects.all()
    context = {
        'curr_user': curr_user,
        'quotes': quotes,
    }
    return render(request, "quotations/main.html", context)

def create(request):
    if request.session['current_user'] == None:
        return redirect('/logout')
    curr_user = User.objects.get(id=request.session['current_user'])
    errors = Quote.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    quote = Quote.objects.create(author = request.POST['author'], quote = request.POST['quote'], uploader = curr_user)
    return redirect('/quotes')

def show_user(request, user_id):
    if request.session['current_user'] == None:
        return redirect('/logout')
    selected_user = User.objects.get(id=user_id)
    quotes = selected_user.uploaded_quote.all()
    context = {
        'user': selected_user,
        'quotes': quotes
    }
    return render(request, "quotations/user_quotes.html", context)

def like(request, user_id, quote_id):
    if request.session['current_user'] == None:
        return redirect('/logout')
    user = User.objects.get(id=user_id)
    quote = Quote.objects.get(id=quote_id)
    quote.liked_users.add(user)
    return redirect('/quotes')

def unlike(request, user_id, quote_id):
    if request.session['current_user'] == None:
        return redirect('/logout')
    user = User.objects.get(id=user_id)
    quote = Quote.objects.get(id=quote_id)
    quote.liked_users.remove(user)
    return redirect('/quotes')

def delete_quote(request, quote_id):
    if request.session['current_user'] == None:
        return redirect('/logout')
    quote = Quote.objects.get(id = quote_id)
    quote.delete()
    return redirect("/quotes")