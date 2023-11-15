import locale
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# Create your models here.
class Ticket(models.Model):
    name_validator = RegexValidator(
        regex='^[a-zA-Z0-9 ]+$',
        message='Name must only contain letters, numbers, and spaces.',
    )

    name = models.CharField(max_length=200, validators=[name_validator])
    winning_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(9999999999.99)]
    )
    cost = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(10.00)]
    )

    def formatted_winning_amount(self):
        # Set the locale to use commas for thousands separator
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        # Format the winning_amount using commas
        formatted_amount = locale.format_string("%.2f", self.winning_amount, grouping=True)

        return formatted_amount

    def __str__(self) -> str:
        return self.name