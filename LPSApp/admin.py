from django.contrib import admin
from .models import *
from django import forms

# Register your models here.
admin.site.register(Ticket)
admin.site.register(UserProfile)
admin.site.register(SavedCard)
admin.site.register(PreviousWinner)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['claimed']

class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ['display_order_id', 'claimed']

    def display_order_id(self, obj):
        return obj.id

    display_order_id.short_description = 'Order ID'

    def get_queryset(self, request):
        # Filter orders where winner is True
        return super().get_queryset(request).filter(winner=True)

admin.site.register(Order, OrderAdmin)