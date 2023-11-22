from django.shortcuts import render, redirect
from .models import *
from .functions.helper import *
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

@login_required(login_url='/login/')
def index(request):
    if request.method == 'GET':
        ticket_data = Ticket.objects.all().order_by('name')
        main_data = {
            "tickets": ticket_data,
            "loggedIn":True,
        }
        return render(request, 'index.html', main_data)

def browse(request):
    if request.method == 'GET':
        ticket_data = Ticket.objects.all().order_by('name')
        is_logged_in = request.user != AnonymousUser()
        main_data = {
            "tickets": ticket_data,
            "loggedIn": is_logged_in,
        }
        return render(request, 'browse.html', main_data)

def loginUser(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        firstName = request.POST.get('firstName')
        username = request.POST.get('email')
        password = request.POST.get('password')
        if firstName:
            try:
                lastName = request.POST.get('lastName')
                email = request.POST.get('email')
                confirmPassword = request.POST.get('confirmpassword')
                if password == confirmPassword:
                    user = User.objects.create_user(email, email, password)
                    user.first_name = firstName
                    user.last_name = lastName
                    user.save()
                    print('created')
                    login(request, user)
                    return redirect('/home/')
                else:
                    print('Passwords dont match')
                    return render(request, 'login.html',{'passwordError':True})
            except Exception as e:
                print("Error creating")
                return render(request, 'login.html',{'emailError':True})
        if username:
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                print('logged in')
                return redirect('/home/')
            else:
                print('No User')
                return render(request, 'login.html',{'noUser':True})
        else:
            logout(request)
            print('logged out')
            return redirect('/login/')

def previousWinner(request):
    return render(request, 'previousWinner.html')

def privacy(request):
    is_logged_in = request.user != AnonymousUser()
    main_data = {
        "loggedIn": is_logged_in,
    }
    return render(request, 'privacy.html', main_data)

@login_required(login_url='/login/')
def profile(request):
    main_data = {
        "loggedIn":True,
    }
    return render(request, 'profile.html', main_data)

@login_required(login_url='/login/')
def purchaseHistory(request):
    main_data = {
        "loggedIn":True,
    }
    return render(request, 'purchaseHistory.html', main_data)

def responsible(request):
    is_logged_in = request.user != AnonymousUser()
    main_data = {
        "loggedIn": is_logged_in,
    }
    return render(request, 'responsible.html', main_data)

def terms(request):
    is_logged_in = request.user != AnonymousUser()
    main_data = {
        "loggedIn": is_logged_in,
    }
    return render(request, 'terms.html', main_data)
