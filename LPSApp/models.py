import locale
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils import timezone

# Create your models here.
class Ticket(models.Model):
    name = models.CharField(max_length=200)
    winning_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(9999999999.99)]
    )
    cost = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(10.00)]
    )
    next_draw_date = models.DateTimeField(default=timezone.now, null=True)
    previous_draw_date = models.DateTimeField(default=timezone.now, null=True)
    previuous_draw_number_1 = models.IntegerField(default=None, null=True)
    previuous_draw_number_2 = models.IntegerField(default=None, null=True)
    previuous_draw_number_3 = models.IntegerField(default=None, null=True)
    previuous_draw_number_4 = models.IntegerField(default=None, null=True)
    previuous_draw_number_5 = models.IntegerField(default=None, null=True)

    def formatted_winning_amount(self):
        # Set the locale to use commas for thousands separator
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        # Format the winning_amount using commas
        formatted_amount = locale.format_string("%.2f", self.winning_amount, grouping=True)

        return formatted_amount

    def __str__(self) -> str:
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.CharField(max_length=20,default=None, null=True)
    # Add additional fields related to the user

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class SavedCard(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=255)
    expiration_date = models.DateField()

    def formatted_expiration_date(self):
        # Format the expiration date to display as MM/YYYY
        formatted_date = self.expiration_date.strftime('%m/%Y')
        return formatted_date

    def formatted_card_number(self):
        # Add spaces every 4 characters
        formatted_number = ' '.join([self.card_number[i:i+4] for i in range(0, len(self.card_number), 4)])
        return formatted_number

    def last_four_digits(self):
        return self.card_number[-4:]

    def __str__(self):
        return f"Card ending in {self.last_four_digits()} for {self.user_profile.user.username}"
    
class Order(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    ticket = models.CharField(max_length=50, default=None, null=True)
    ticketCost = models.CharField(max_length=10, default=None, null=True)
    number_1 = models.IntegerField(default=None, null=True)
    number_2 = models.IntegerField(default=None, null=True)
    number_3 = models.IntegerField(default=None, null=True)
    number_4 = models.IntegerField(default=None, null=True)
    number_5 = models.IntegerField(default=None, null=True)
    winner = models.BooleanField(default=False,null=True)
    winning_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(9999999999.99)],
        null=True, default=0
    )
    claimed = models.BooleanField(default=False,null=True)
    # TODO Add more order info

    def __str__(self):
        return f"Order {self.id} by {self.user_profile.user.username} on {self.order_date}"
    
    def formatted_winning_amount(self):
        # Set the locale to use commas for thousands separator
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        # Format the winning_amount using commas
        formatted_amount = locale.format_string("%.2f", self.winning_amount, grouping=True)

        return formatted_amount
    
class PreviousWinner(models.Model):
    name = models.CharField(max_length=200)
    winning_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(9999999999.99)],
        null=True, default=0
    )
    win_date = models.DateTimeField(default=timezone.now, null=True)
    ticketType = models.CharField(max_length=200)

    def formatted_date(self):
        # Format the win_date to display only month and year
        formatted_date = self.win_date.strftime("%B %Y")

        return formatted_date

    def __str__(self):
        return self.name
    
    def formatted_winning_amount(self):
        # Set the locale to use commas for thousands separator
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        # Format the winning_amount using commas
        formatted_amount = locale.format_string("%.2f", self.winning_amount, grouping=True)

        return formatted_amount