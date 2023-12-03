from django.urls import path
from . import views

urlpatterns = [
    #----------------Pages----------------
    path('',views.loginUser, name='login'),
    path('home/',views.index, name='home'),
    path('browse/',views.browse, name='browse'),
    path('login/',views.loginUser, name='login'),
    path('previous-winner/',views.previousWinner, name='previousWinner'),
    path('privacy/',views.privacy, name='privacy'),
    path('profile/',views.profile, name='profile'),
    path('purchase/<str:ticket>/', views.purchase, name='purchase'),
    path('purchase-history/',views.purchaseHistory, name='purchaseHistory'),
    path('purchase-history/<str:id>/',views.purchaseHistory, name='purchaseHistory'),
    path('responsible/',views.responsible, name='responsible'),
    path('terms/',views.terms, name='terms'),
]
