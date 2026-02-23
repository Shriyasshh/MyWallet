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
    # COLOR_CHOICES = [
    #     ('#0F172A', 'Dark Navy'),
    #     ('#10B981', 'Emerald Green'),
    #     ('#38BDF8', 'Sky Blue'),
    #     ('#8B5CF6', 'Purple'),
    #     ('#EF4444', 'Red'),
    #     ('#F59E0B', 'Amber'),
    #     ('#EC4899', 'Pink'),
    #     ('#14B8A6', 'Teal'),
    #     ('#6366F1', 'Indigo'),
    #     ('#F97316', 'Orange'),
    # ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=50,choices = ACCOUNT_CHOICES, default='Cash')
    accountName = models.CharField(max_length=50)
    accountBalance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(
    max_length=10,
    choices=[
        ('INR', '₹'),('USD', '$'),('EUR', '€'),('GBP', '£'),('JPY', '¥'),('CAD', 'C$'),('AUD', 'A$'),
    ],default='INR')

    bankName = models.CharField(max_length=100, blank=True, null=True)
    accountNumber = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    # cardColor = models.CharField(max_length=7,choices=COLOR_CHOICES,default='#0F172A')    
    icon = models.CharField(max_length=50, choices=ICON_CHOICES ,default='bi bi-cash-stack')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.accountName
    

from django.db import models
from django.contrib.auth.models import User
from .models import AddAccount


class Transaction(models.Model):

    PAYMENT_TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
        ('Transfer', 'Transfer'),
    ]
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Shopping', 'Shopping'),
        ('Bills', 'Bills'),
        ('Salary', 'Salary'),
        ('Investment', 'Investment'),
        ('Other', 'Other'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(AddAccount, on_delete=models.CASCADE)

    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)

    account = models.ForeignKey(AddAccount,on_delete=models.CASCADE)

    description = models.TextField(blank=True, null=True)

    payee = models.CharField(max_length=100,blank=True,null=True)

    # is_recurring = models.BooleanField(default=False)

    # receipt = models.ImageField(upload_to='receipts/',blank=True,null=True)
    to_account = models.ForeignKey(AddAccount,on_delete=models.CASCADE,related_name='transfer_to',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.payment_type == 'Income':

            self.account.accountBalance += self.amount
            self.account.save()

        elif self.payment_type == 'Expense':

            self.account.accountBalance -= self.amount
            self.account.save()

        elif self.payment_type == 'Transfer':

            if not self.to_account:
                raise ValueError("Transfer requires a destination account")

            if self.account == self.to_account:
                raise ValueError("Source and destination account cannot be the same")

            # subtract from source
            self.account.accountBalance -= self.amount
            self.account.save()

            # add to destination
            self.to_account.accountBalance += self.amount
            self.to_account.save()
        super().save(*args, **kwargs)