from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import LoginAccountOwnership, LoginAccounts


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


class LoginAccountOwnershipAdminForm(forms.ModelForm):
    login_account_name = forms.CharField(
        max_length=50,
        help_text='Login server account name (e.g. "JohnEQ"). The numeric ID is resolved automatically.',
    )

    class Meta:
        model = LoginAccountOwnership
        fields = ['user', 'login_account_name']

    def clean_login_account_name(self):
        name = self.cleaned_data['login_account_name'].strip()
        try:
            ls_account = LoginAccounts.objects.using('login_server_database').get(account_name=name)
        except LoginAccounts.DoesNotExist:
            raise forms.ValidationError(f'No login server account found with name "{name}".')
        except LoginAccounts.MultipleObjectsReturned:
            raise forms.ValidationError(f'Multiple login accounts match "{name}" — be more specific.')
        # Stash the resolved ID so save() can use it
        self._resolved_ls_id = ls_account.id
        return name

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.login_account_id = self._resolved_ls_id
        if commit:
            instance.save()
        return instance


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
