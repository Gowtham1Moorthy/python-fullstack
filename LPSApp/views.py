from django.shortcuts import render, redirect
from .models import *
from .functions.helper import *
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import CardForm

# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

@login_required(login_url='/login/')
def index(request):
    if request.method == 'GET':
        ticket_data = Ticket.objects.all().order_by('name')
        purchased = request.GET.get('purchased', False)
        print(purchased)
        main_data = {
            "tickets": ticket_data,
            "loggedIn":True,
            'purchased': purchased,
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
    # TODO Add a post request to handle buying stuff (redirect to puchase screen)

def loginUser(request):
    # TODO on all errors make sure it jumps to that error on the page
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
                    # TODO implement dob checker
                    user = User.objects.create_user(email, email, password)
                    user.first_name = firstName
                    user.last_name = lastName
                    user.save()
                    UserProfile.objects.create(user=user)
                    print('created')
                    login(request, user)
                    return redirect('/home/')
                else:
                    print('Passwords dont match')
                    return render(request, 'login.html',{'passwordError':True})
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
    return render(request, 'previousWinner.html')

def privacy(request):
    is_logged_in = request.user != AnonymousUser()
    main_data = {
        "loggedIn": is_logged_in,
    }
    return render(request, 'privacy.html', main_data)

@login_required(login_url='/login/')
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
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
                messages.success(request, 'Card updated successfully!') # TODO Change this to not be a message
            else:
                # If no card exists, create a new one
                SavedCard.objects.create(
                    user_profile=user_profile,
                    card_number=card_data['card_number'],
                    cardholder_name=card_data['cardholder_name'],
                    expiration_date=card_data['expiration_date']
                    # Add other fields related to the card information
                )
                messages.success(request, 'Card saved successfully!') # TODO Change this to not be a message
            return redirect('profile') # ? is this needed
        else:
            messages.error(request, 'Error saving/updating card. Please check the form.') # TODO Change this to not be a message

    main_data = {
        "loggedIn": True,
        'user_profile': user_profile,
        'form': CardForm() if not user_profile.savedcard_set.exists() else None
    }
    return render(request, 'profile.html', main_data)

@login_required(login_url='/login/')
def purchase(request, ticket):
    user_profile = UserProfile.objects.get(user=request.user)
    cardInfo = SavedCard.objects.get(user_profile=user_profile)
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
            Order.objects.create(
                user_profile=user_profile,
                ticket=ticket,
                ticketCost=ticketCost
            )
            #TODO Send email reciept
            print('Purchased')
            return redirect('/home/?purchased=True')
            # else
            # redirect(f'/purchase/{ticket}')
    main_data = {
        "loggedIn": True,
        'ticket': ticketInfo,
        'cardInfo':cardInfo,
        'tax': tax,
        'ticketCost': ticketCost,
        'ticketLimit': ticketLimit,
        'cardUpdated': cardUpdated,
        'cardError': cardError,
    }
    return render(request, 'purchase.html', main_data)


@login_required(login_url='/login/')
def purchaseHistory(request):
    user_profile = UserProfile.objects.get(user=request.user)
    orders = Order.objects.filter(user_profile=user_profile).order_by('-order_date')
    main_data = {
        "loggedIn":True,
        "user_profile": user_profile,
        "orders": orders,
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
