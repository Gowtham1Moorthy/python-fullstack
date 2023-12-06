from django.contrib import admin
from .models import *
from django import forms

# Register your models here.
admin.site.register(Ticket)
admin.site.register(UserProfile)
admin.site.register(SavedCard)
admin.site.register(Order)
admin.site.register(PreviousWinner)

class ClaimedOrderForm(forms.ModelForm):
    class Meta:
        model = ClaimedOrder
        fields = ['claimed']

class ClaimedOrderAdmin(admin.ModelAdmin):
    form = ClaimedOrderForm
    list_display = ['display_order_id', 'claimed']

    def display_order_id(self, obj):
        return obj.order.id

    display_order_id.short_description = 'Order ID'

admin.site.register(ClaimedOrder, ClaimedOrderAdmin)