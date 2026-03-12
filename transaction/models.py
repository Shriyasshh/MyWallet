from django.db import models
from django.contrib.auth.models import User
from accounts.models import AddAccount


class Transaction(models.Model):

    PAYMENT_TYPE_CHOICES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
        ('transfer', 'Transfer'),
        ('borrowed', 'Borrowed'),
        ('lent', 'Lent'),
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
        ('borrowed', 'Borrowed'),
        ('lent', 'Lent'),
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
    
class Debt(models.Model):
    
    DEBT_TYPE_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('lent', 'Lent'),
    ]
    RELATION_CHOICES = [
        ('Family', 'Family'),
        ('Friend', 'Friend'),
        ('Colleague', 'Colleague'),
        ('Bank', 'Bank'),
        ('Other', 'Other'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    debtType = models.CharField(max_length=50,choices=DEBT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    borrow_lent_from = models.CharField(max_length=100)
    relation = models.CharField(max_length=50,choices=RELATION_CHOICES)
    contact = models.CharField(max_length=100, blank=True, null=True)
    linkedAccount = models.ForeignKey(AddAccount, on_delete=models.CASCADE)
    date = models.DateField()
    duedate = models.DateField()
    note = models.TextField(blank=True, null=True)
    repayment = models.CharField(max_length=50,blank=True,null=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs): 
        account = self.linkedAccount 
        # determine if this is a new record before saving
        is_new = self.pk is None

        # update linked account balance according to debt type
        if self.debtType == 'borrowed': 
            account.accountBalance += self.amount 
            account.save() 
        elif self.debtType == 'lent': 
            account.accountBalance -= self.amount 
            account.save() 

        # persist the Debt itself
        super().save(*args, **kwargs)

        # when a new debt is created, also record a matching transaction
        if is_new:
            # note text should mirror the logic used in the view
            if self.debtType == 'borrowed':
                t_note = f"Money {self.debtType} from {self.borrow_lent_from} till {self.duedate}"
            else:
                t_note = f"Money {self.debtType} to {self.borrow_lent_from} till {self.duedate}"

            Transaction.objects.create(
                user=self.user,
                payment_type=self.debtType,
                amount=self.amount,
                category=self.debtType,
                account=self.linkedAccount,
                date=self.date,
                time="12:00",
                payee=self.borrow_lent_from,
                note=t_note,
            )
