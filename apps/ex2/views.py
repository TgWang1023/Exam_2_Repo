from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def main(request):
    return render(request, 'ex2/main.html')

def register(request):
    request.session['register'] = True
    request.session['login'] = False
    if request.method == 'POST':
        errors = User.objects.reg_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], bday = request.POST['bday'], pass_hs = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        user.save()
        request.session['logged_in'] = True
        request.session['name'] = user.first_name
        request.session['id'] = user.id
        return redirect('/quotes')
    else:
        return redirect('/')

def login(request):
    request.session['register'] = False
    request.session['login'] = True
    if request.method == 'POST':
        errors = User.objects.login_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        request.session['logged_in'] = True
        request.session['name'] = User.objects.get(email = request.POST['login_email']).first_name
        request.session['id'] = User.objects.get(email = request.POST['login_email']).id
        return redirect('/quotes')
    else:
        return redirect('/')

def quotes(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
        return redirect('/')
    else:
        if request.session['logged_in'] == False:
            return redirect('/')

    context = { 
        'name': request.session['name'],
        'quotes': Quote.objects.all()
    }

    return render(request, 'ex2/quotes.html', context)

def quote_actions(request):
    if request.method == 'POST':
        if request.POST['buttons'] == 'like':
            if not Quote.objects.get(id = request.POST['quote_id']).user_liked.filter(id = request.session['id']).exists():
                q = Quote.objects.get(id = request.POST['quote_id'])
                q.likes += 1
                q.user_liked.add(User.objects.get(id = request.session['id']))
                q.save()
        elif request.POST['buttons'] == 'delete':
            Quote.objects.get(id = request.POST['quote_id']).delete()
        return redirect('/quotes')
    else:
        return redirect('/')

def add_quote(request):
    if request.method == 'POST':
        errors = Quote.objects.quote_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/quotes')
    
        Quote.objects.create(author = request.POST['author_input'], content = request.POST['quote_input'], likes = 0, user = User.objects.get(id = request.session['id']))
        return redirect('/quotes')
    else:
        return redirect('/')

def edit(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
        return redirect('/')
    else:
        if request.session['logged_in'] == False:
            return redirect('/')

    context = {
        'first_name': User.objects.get(id = request.session['id']).first_name,
        'last_name': User.objects.get(id = request.session['id']).last_name,
        'email': User.objects.get(id = request.session['id']).email
    }
    return render(request, 'ex2/account_edit.html', context)

def update(request):
    if request.method == 'POST':
        errors = User.objects.edit_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit')
        
        user = User.objects.get(id = request.session['id'])
        user.first_name = request.POST['fn_input']
        user.last_name = request.POST['ln_input']
        user.email = request.POST['email_input']
        user.save()
        request.session['name'] = request.POST['fn_input']
        return redirect('/quotes')
    else:
        return redirect('/')

def display(request, id):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
        return redirect('/')
    else:
        if request.session['logged_in'] == False:
            return redirect('/')

    context = {
        'user': User.objects.get(id = id),
        'quotes': User.objects.get(id = id).quotes.all()
    }

    return render(request, 'ex2/user_display.html', context)

def logout(request):
    if request.method == 'POST':
        request.session.clear()
        return redirect('/')
    else:
        return redirect('/')

def reset(request):
    request.session.clear()
    return redirect('/')