from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AddAccount(models.Model):
    ACCOUNT_CHOICES = [
        ('Cash', 'Cash'),
        ('Bank', 'Bank Account'),
        ('Credit Card', 'Credit Card'),
        ('Savings', 'Savings Goal'),
        # ('Investment', 'Investment'),
        # ('E-Wallet', 'E-Wallet'),
    ]
    ICON_CHOICES = [
        ('bi bi-cash-stack', 'Cash'),
        ('bi bi-building-fill', 'Bank'),
        ('bi bi-credit-card-2-front-fill', 'Credit Card'),
        ('bi bi-safe2-fill', 'Safe'),
        ('bi bi-graph-up-arrow', 'Investment'),
        ('bi bi-phone-fill', 'Phone'),
        ('bi bi-piggy-bank-fill', 'Piggy Bank'),
        ('bi bi-wallet2', 'Wallet'),
        ('bi bi-star-fill', 'Star'),
        ('bi bi-globe', 'Globe'),
]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=50,choices = ACCOUNT_CHOICES, default='Cash')
    accountName = models.CharField(max_length=50)
    accountBalance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('INR', 'INR'), ('JPY', 'JPY'), ('CAD', 'CAD'), ('AUD', 'AUD')], default='USD')
    bankName = models.CharField(max_length=100, blank=True, null=True)
    accountNumber = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    cardColor = models.CharField(max_length=7, default='#0F172A')
    icon = models.CharField(max_length=50, choices=ICON_CHOICES ,default='bi bi-cash-stack')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.accountName