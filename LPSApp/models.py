import locale
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Ticket(models.Model):
    name = models.CharField(max_length=200)
    winning_amount = models.DecimalField(
            max_digits=12, decimal_places=2,
            validators=[MinValueValidator(0.00), MaxValueValidator(9999999999.99)]
        )  # Maximum winnings set to 3-digit billions with 2 decimal places
    cost = models.DecimalField(
            max_digits=4, decimal_places=2,
            validators=[MinValueValidator(0.00), MaxValueValidator(10.00)]
        )  # Maximum cost set to 10 with 2 decimal places

    def formatted_winning_amount(self):
        # Set the locale to use commas for thousands separator
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        # Format the winning_amount using commas
        formatted_amount = locale.format_string("%.2f", self.winning_amount, grouping=True)

        return formatted_amount

    def __str__(self) -> str:
        return self.name