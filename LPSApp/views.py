from django.shortcuts import render
from django.utils.text import slugify
from .models import *
from .functions.helper import *

# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

def index(request):
    if request.method == 'GET':
        ticket_data = Ticket.objects.all().order_by('name')
        main_data = {
            "tickets": ticket_data,
            "loggedIn":True,
        }
        return render(request, 'index.html', main_data)

def showLotto(request, name=None):
    # Add if logged in part
    if name:
        name_deslug = deslugify(name)
        try:
            ticket_item = Ticket.objects.get(name=name_deslug)
        except Ticket.DoesNotExist:
            print(Ticket.DoesNotExist)
            ticket_item = None
    else:
        ticket_item = None

    return render(request, 'ticket_item.html', {"ticket_item": ticket_item})

def browse(request):
    # Add if logged in part
    if request.method == 'GET':
        ticket_data = Ticket.objects.all().order_by('name')
        main_data = {
            "tickets": ticket_data,
            "loggedIn":True,
        }
        return render(request, 'browse.html', main_data)
    
def login(request):
    return render(request, 'login.html')

def previousWinner(request):
    return render(request, 'previousWinner.html')

def privacy(request):
    # Add if logged in part
    return render(request, 'privacy.html')

def profile(request):
    main_data = {
        "loggedIn":True,
    }
    return render(request, 'profile.html', main_data)

def purchaseHistory(request):
    main_data = {
        "loggedIn":True,
    }
    return render(request, 'purchaseHistory.html', main_data)

def responsible(request):
    # Add if logged in part
    return render(request, 'responsible.html')
