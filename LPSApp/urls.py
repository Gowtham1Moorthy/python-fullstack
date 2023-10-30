from django.urls import path
from . import views

urlpatterns = [
    #----------------Pages----------------
    path('',views.index, name='index'),
    path('index/',views.index, name='index'),
    path('browse/',views.browse, name='browse'),
    path('previousWinner/',views.previousWinner, name='previousWinner'),
    path('profile/',views.profile, name='profile'),
    path('previousWinner/',views.previousWinner, name='previousWinner'),
    path('purchaseHistory/',views.purchaseHistory, name='purchaseHistory'),
    path('search/',views.search, name='search'),
]
