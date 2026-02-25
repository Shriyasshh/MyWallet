# from django import forms
# from .models import Transaction

# class TransactionForm(forms.ModelForm):

#     class Meta:
#         model = Transaction
#         fields = [
#             'payment_type',
#             'amount',
#             'category',
#             'account',
#             'to_account',
#             'date',
#             'time',
#             'note',
#             'payee'
#         ]

#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'}),
#             'time': forms.TimeInput(attrs={'type': 'time'}),
#             'note': forms.Textarea(attrs={'rows': 2}),
#         }