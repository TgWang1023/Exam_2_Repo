from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
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
        return redirect('/success')
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
        return redirect('/success')
    else:
        return redirect('/')

def success(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
        return redirect('/')
    else:
        if request.session['logged_in'] == False:
            return redirect('/')

    context = { 
        'name': request.session['name']
    }

    return render(request, 'ex2/success.html', context)

def logout(request):
    if request.method == 'POST':
        request.session.clear()
        return redirect('/')
    else:
        return redirect('/')

def reset(request):
    request.session.clear()
    return redirect('/')