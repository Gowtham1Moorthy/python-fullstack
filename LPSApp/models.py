import locale
from django.db import models
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
    next_draw_date = models.DateField(default=timezone.now, null=True)
    previous_draw_date = models.DateField(default=timezone.now, null=True)
    previuous_draw_number_1 = models.IntegerField(default=None, null=True)
    previuous_draw_number_2 = models.IntegerField(default=None, null=True)
    previuous_draw_number_3 = models.IntegerField(default=None, null=True)
    previuous_draw_number_4 = models.IntegerField(default=None, null=True)
    previuous_draw_number_5 = models.IntegerField(default=None, null=True)
    previuous_draw_number_6 = models.IntegerField(default=None, null=True)
    powerball = models.BooleanField(default=False, null=True)

    def formatted_winning_amount(self):
        # Set the locale to use commas for thousands separator
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        # Format the winning_amount using commas
        formatted_amount = locale.format_string("%.2f", self.winning_amount, grouping=True)

        return formatted_amount

    def __str__(self) -> str:
        return self.name