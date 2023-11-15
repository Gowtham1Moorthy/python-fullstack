from django.urls import path
from . import views

urlpatterns = [
    #----------------Pages----------------
    path('',views.index, name='home'),
    path('home/',views.index, name='home'),
    path('home/<str:name>',views.showLotto, name='home'),
    path('browse/',views.browse, name='browse'),
    path('login/',views.login, name='login'),
    path('previous-winner/',views.previousWinner, name='previousWinner'),
    path('profile/',views.profile, name='profile'),
    path('purchase-history/',views.purchaseHistory, name='purchaseHistory'),
    path('search/',views.search, name='search'),
]
