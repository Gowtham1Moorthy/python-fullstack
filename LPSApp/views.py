from django.shortcuts import render

# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

def index(request):
    return render(request, 'index.html')