from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Old Password"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password"
    )
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New Password"
    )
    def __init__(self, user, *args, **kwargs):
        # self.user =  kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user=user

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')

        if old_password and not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect.")
        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise forms.ValidationError("New passwords do not match.")

        return cleaned_data