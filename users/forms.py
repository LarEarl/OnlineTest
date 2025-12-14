from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned = super().clean()
        pwd1 = cleaned.get('password1')
        pwd2 = cleaned.get('password2')
        if pwd1 != pwd2:
            raise forms.ValidationError('Пароли не совпадают.')
        if pwd1:
            validate_password(pwd1)
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    identifier = forms.CharField(label='Username или Email')
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, initial=False)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'avatar']
