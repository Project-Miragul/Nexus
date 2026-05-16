from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import LoginAccounts


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.username = self.cleaned_data["username"].title()
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewLSAccountForm(ModelForm):
    account_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = LoginAccounts
        fields = ('account_name', 'account_password', 'account_email')


class UpdateLSAccountForm(ModelForm):

    class Meta:
        model = LoginAccounts
        fields = ('account_password', 'account_email')


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
