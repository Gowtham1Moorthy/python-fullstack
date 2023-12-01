from django import forms

class CardForm(forms.Form):
    card_number = forms.CharField(max_length=16)
    cardholder_name = forms.CharField(max_length=255)
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'MM/YY'}), input_formats=['%m/%y'])
    # Add other fields if necessary (e.g., CVV)
