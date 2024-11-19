from django.shortcuts import render, redirect
from .models import *
from .functions.helper import *
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CardForm
import datetime
import random

# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)
def admindashboard(request):
    user = User.objects.all().count()
    tick = Ticket.objects.all().count()
    ord = Order.objects.all().count()
    print(tick)
    context ={
        'user' :user,
        'tick' : tick,
        'ord' : ord,

    }
    return render(request,'admin_dash.html', context)

@login_required(login_url='/login/')
def index(request):
    if request.method == 'GET':
        ticket_data = Ticket.objects.all().order_by('name')
        purchased = request.GET.get('purchased', False)
        admin = request.user.is_staff
        main_data = {
            "tickets": ticket_data,
            "loggedIn":True,
            'purchased': purchased,
            'admin': admin,
        }
        return render(request, 'index.html', main_data)

def browse(request):
    if request.method == 'GET':
        ticket_data = Ticket.objects.all().order_by('name')
        is_logged_in = request.user != AnonymousUser()
        admin = request.user.is_staff
        main_data = {
            "tickets": ticket_data,
            "loggedIn": is_logged_in,
            'admin': admin,
        }
        return render(request, 'browse.html', main_data)

# views.py

from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(mail):
    subject = 'Welcome to Our Platform'
    message = 'Thank you for signing up!'
    recipient_list = [mail]  # List of recipients
    email_from = settings.DEFAULT_FROM_EMAIL
    
    send_mail(subject, message, email_from, recipient_list)


def loginUser(request):
    ## TODO on all errors make sure it jumps to that error on the page
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        firstName = request.POST.get('firstName')
        username = request.POST.get('email')
        password = request.POST.get('password')
        if firstName:
            try:
                lastName = request.POST.get('lastName')
                birthday = request.POST.get('birthday')
                birthdate = datetime.datetime.strptime(birthday, "%m/%d/%y")
                today = datetime.datetime.today()
                age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
                email = request.POST.get('email')
                confirmPassword = request.POST.get('confirmpassword')
                if password == confirmPassword and age>=18:
                    user = User.objects.create_user(email, email, password)
                    user.first_name = firstName
                    user.last_name = lastName
                    user.save()
                    UserProfile.objects.create(user=user, birthday=birthday)
                    print('created')
                    send_welcome_email(email)
                    login(request, user)
                    return redirect('/')
                else:
                    if password != confirmPassword:
                        print('Passwords dont match')
                        return render(request, 'login.html',{'passwordError':True})
                    else:
                        print('User is not of legal age.')
                        return render(request, 'login.html',{'ageError':True})
            except Exception as e:
                print("Error creating:", e)
                return render(request, 'login.html',{'emailError':True})
        if username:
            user = authenticate(request, username=username, password=password)
            print(f"Username: {user}")
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
    is_logged_in = request.user != AnonymousUser()
    previousWinners = PreviousWinner.objects.all().order_by('-win_date')
    admin = request.user.is_staff
    main_data = {
        "loggedIn": is_logged_in,
        'previousWinners': previousWinners,
        'admin': admin,
    }
    return render(request, 'previousWinner.html', main_data)

def privacy(request):
    is_logged_in = request.user != AnonymousUser()
    admin = request.user.is_staff
    main_data = {
        "loggedIn": is_logged_in,
        'admin': admin,
    }
    return render(request, 'privacy.html', main_data)

@login_required(login_url='/login/')
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    admin = request.user.is_staff
    try:
        cardInfo = SavedCard.objects.get(user_profile=user_profile)
    except Exception as e:
        cardInfo = None
    cardUpdated = False
    cardError = False
    cardSaved = False
    
    if request.method == 'POST':
        r = SavedCard.objects.create(
                    user_profile=user_profile,
                    card_number=request.POST.get("card_number"),
                    cardholder_name=request.POST.get("cardholder_name"),
                    # Add other fields related to the card information
                )
        print('Card saved successfully!')
        r.save()
        cardSaved = True
        cardInfo = SavedCard.objects.get(user_profile=user_profile)
    main_data = {
        "loggedIn": True,
        'user_profile': user_profile,
        'cardInfo': cardInfo,
        'cardUpdated': cardUpdated,
        'cardSaved': cardSaved,
        'cardError': cardError,
        'admin': admin,
    }
    return render(request, 'profile.html', main_data)

@login_required(login_url='/login/')
def purchase(request, ticket):
    user_profile = UserProfile.objects.get(user=request.user)
    admin = request.user.is_staff
    try:
        cardInfo = SavedCard.objects.get(user_profile=user_profile)
    except Exception as e:
        cardInfo = None
    ticketInfo = Ticket.objects.get(name=ticket)
    tax = round(float(ticketInfo.cost) * .0825, 2)
    ticketCost = round(float(ticketInfo.cost) + tax,2)
    ticketLimit = False
    orders = Order.objects.filter(user_profile=user_profile)
    if len(orders) >= 10:
        print('Cannot be purchased, ticket limit set')
        ticketLimit = True

    cardUpdated = False
    cardError = False
    cardExpError = False

    if request.method == 'POST':
        cardNum = request.POST.get('card_number')
        if cardNum:
            form = CardForm(request.POST)
            if form.is_valid():
                card_data = form.cleaned_data
                # Check if the user already has a saved card
                existing_card = user_profile.savedcard_set.first()
                if existing_card:
                    # If a card exists, update its details
                    existing_card.card_number = card_data['card_number']
                    existing_card.cardholder_name = card_data['cardholder_name']
                    existing_card.expiration_date = card_data['expiration_date']
                    # Add other fields related to the card information
                    existing_card.save()
                    print('Card updated successfully!')
                    cardUpdated = True
                    cardInfo = SavedCard.objects.get(user_profile=user_profile)
                else:
                    # If no card exists, create a new one
                    SavedCard.objects.create(
                        user_profile=user_profile,
                        card_number=card_data['card_number'],
                        cardholder_name=card_data['cardholder_name'],
                        expiration_date=card_data['expiration_date']
                        # Add other fields related to the card information
                    )
                    print('Card saved successfully!')
                redirect(f'/purchase/{ticket}')
            else:
                print('Error saving/updating card.')
                cardError = True
        else:
            # Check with bank
            # if returns true:

            numbers = random.sample(range(1, 69 + 1), 5)
            Order.objects.create(
                user_profile=user_profile,
                ticket=ticket,
                ticketCost=ticketCost,
                number_1 = numbers[0],
                number_2 = numbers[1],
                number_3 = numbers[2],
                number_4 = numbers[3],
                number_5 = numbers[4],
            )
            #TODO Send email reciept
            print('Purchased')
            return redirect('/')
        
            if cardInfo.expiration_date > datetime.date.today():
                numbers = random.sample(range(1, 69 + 1), 5)
                Order.objects.create(
                    user_profile=user_profile,
                    ticket=ticket,
                    ticketCost=ticketCost,
                    number_1 = numbers[0],
                    number_2 = numbers[1],
                    number_3 = numbers[2],
                    number_4 = numbers[3],
                    number_5 = numbers[4],
                )
                #TODO Send email reciept
                print('Purchased')
                return redirect('/')
            else:
                cardExpError = True
    main_data = {
        "loggedIn": True,
        'ticket': ticketInfo,
        'cardInfo':cardInfo,
        'tax': tax,
        'ticketCost': ticketCost,
        'ticketLimit': ticketLimit,
        'cardUpdated': cardUpdated,
        'cardError': cardError,
        'cardExpError': cardExpError,
        'admin': admin,
    }
    return render(request, 'purchase.html', main_data)


@login_required(login_url='/login/')
def purchaseHistory(request, id=None):
    user_profile = UserProfile.objects.get(user=request.user)
    admin = request.user.is_staff
    orders = Order.objects.filter(user_profile=user_profile).order_by('-order_date')
    if request.method == 'GET':
        for order in orders:
            matchedNums = 0
            try:
                ticket = Ticket.objects.get(name=order.ticket)
                if order.order_date < ticket.previous_draw_date and not order.claimed:
                    ticketNumbers = [
                        ticket.previous_draw_number_1,
                        ticket.previous_draw_number_2,
                        ticket.previous_draw_number_3,
                        ticket.previous_draw_number_4,
                        ticket.previous_draw_number_5,
                    ]

                    for i in range(1, 6):
                        if getattr(order, f'number_{i}') in ticketNumbers:
                            matchedNums += 1
                    
                    if matchedNums <= 1:
                        winner = False
                    elif matchedNums == 2:
                        winner= True
                        percent = .01
                    elif matchedNums == 3:
                        winner= True
                        percent = .05
                    elif matchedNums == 4:
                        winner= True
                        percent = .2
                    elif matchedNums == 5:
                        winner= True
                        percent = 1
                    
                    winnings = 0
                    if winner:
                        winnings = float(ticket.winning_amount) * percent
                        if winnings >= 600:
                            try:
                                previousWinner = PreviousWinner.objects.get(name=f'{user_profile.user.first_name} {user_profile.user.last_name}',winning_amount=winnings,win_date=order.order_date, ticket_type=order.ticket)
                            except Exception as e:
                                print(f'at this exception: {e}')
                                PreviousWinner.objects.create(
                                    name=f'{user_profile.user.first_name} {user_profile.user.last_name}',
                                    winning_amount=winnings,
                                    win_date=order.order_date,
                                    ticket_type=order.ticket,
                                )

                    order.winner = winner
                    order.winning_amount = round(winnings, 2)
                    order.save()
            except Exception as e:
                print(e)
                order.ticket = f'{order.ticket} (Discontinued)'
    else:
        order = Order.objects.get(id=id)
        order.claimed = True
        order.save()

        try:
            previousWinner = PreviousWinner.objects.get(name=f'{user_profile.user.first_name} {user_profile.user.last_name}',winning_amount=order.winning_amount,win_date=order.order_date, ticket_type=order.ticket)
        except Exception as e:
            print(f'at this exception: {e}')
            PreviousWinner.objects.create(
                name=f'{user_profile.user.first_name} {user_profile.user.last_name}',
                winning_amount=order.winning_amount,
                win_date=order.order_date,
                ticket_type=order.ticket,
            )

        print('Claimed order')
        return redirect('/purchase-history/')
        
    main_data = {
        "loggedIn":True,
        "user_profile": user_profile,
        "orders": orders,
        'admin': admin,
    }
    return render(request, 'purchaseHistory.html', main_data)

def responsible(request):
    is_logged_in = request.user != AnonymousUser()
    admin = request.user.is_staff
    main_data = {
        "loggedIn": is_logged_in,
        'admin': admin,
    }
    return render(request, 'responsible.html', main_data)

def terms(request):
    is_logged_in = request.user != AnonymousUser()
    admin = request.user.is_staff
    main_data = {
        "loggedIn": is_logged_in,
        'admin': admin,
    }
    return render(request, 'terms.html', main_data)

