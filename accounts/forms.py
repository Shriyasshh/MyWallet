from django import forms

from .models import AddAccount

class AddAccountForm(forms.ModelForm):
    class Meta:
        model = AddAccount
        fields = [
            'accountType',
            'accountName',
            'accountBalance',
            'currency',
            'bankName',
            'accountNumber',
            'description',
            'icon',
        ]