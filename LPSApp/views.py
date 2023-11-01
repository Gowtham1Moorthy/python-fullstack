from django.shortcuts import render
from django.urls import reverse

# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

def index(request):
    return render(request, 'index.html')

def showLotto(request, lotto=None):
    print(lotto)
    return render(request, 'index.html')

def browse(request):
    return render(request, 'browse.html')

def previousWinner(request):
    return render(request, 'previousWinner.html')

def profile(request):
    return render(request, 'profile.html')

def purchaseHistory(request):
    return render(request, 'purchaseHistory.html')

def search(request):
    return render(request, 'search.html')