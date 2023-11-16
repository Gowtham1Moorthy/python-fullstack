from django.urls import path
from . import views

urlpatterns = [
    #----------------Pages----------------
    path('',views.index, name='home'),
    path('home/',views.index, name='home'),
    path('home/<str:name>',views.showLotto, name='home'),
    path('browse/',views.browse, name='browse'),
    path('login/',views.loginUser, name='login'),
    path('previous-winner/',views.previousWinner, name='previousWinner'),
    path('privacy/',views.privacy, name='privacy'),
    path('profile/',views.profile, name='profile'),
    path('purchase-history/',views.purchaseHistory, name='purchaseHistory'),
    path('responsible/',views.responsible, name='responsible'),
]
