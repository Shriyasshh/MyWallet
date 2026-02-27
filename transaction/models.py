from django.db import models
from django.contrib.auth.models import User
from accounts.models import AddAccount


class Transaction(models.Model):

    PAYMENT_TYPE_CHOICES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
        ('transfer', 'Transfer'),
    ]
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Rent', 'Rent'),
        ('Health', 'Health'),
        ('Shopping', 'Shopping'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Travel', 'Travel'),
        ('Education', 'Education'),
        ('Pets', 'Pets'),
        ('Personal', 'Personal'),
        ('Repair', 'Repair'),
        ('Bills', 'Bills'),
        ('Salary', 'Salary'),
        ('Investment', 'Investment'),
        ('Other', 'Other'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    account = models.ForeignKey(AddAccount, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    note = models.TextField(blank=True, null=True)

    payee = models.CharField(max_length=100,blank=True,null=True)

    # is_recurring = models.BooleanField(default=False)

    # receipt = models.ImageField(upload_to='receipts/',blank=True,null=True)
    to_account = models.ForeignKey(AddAccount,on_delete=models.CASCADE,related_name='transfer_to',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        account = self.account
        to_account = self.to_account

        if self.payment_type == 'expense':
            
            if account.accountBalance < self.amount:
                raise ValueError("Insufficient balance")
            
            account.accountBalance -=self.amount
            account.save()

        elif self.payment_type == 'income':
            account.accountBalance +=self.amount
            account.save()

        elif self.payment_type == 'transfer':
            if account.accountBalance < self.amount:
                raise ValueError("Insufficient balance")
            
            account.accountBalance -=self.amount
            account.save()

            to_account.accountBalance +=self.amount
            to_account.save()
        super().save(*args, **kwargs)

            


    def __str__(self):
        return self.payment_type