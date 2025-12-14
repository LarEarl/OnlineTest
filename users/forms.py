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
    first_name = forms.CharField(max_length=150, required=False, label='Имя')
    last_name = forms.CharField(max_length=150, required=False, label='Фамилия')
    
    # Поля для смены пароля (необязательные)
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Оставьте пустым, если не хотите менять'}),
        required=False,
        label='Текущий пароль'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Новый пароль'}),
        required=False,
        label='Новый пароль'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите новый пароль'}),
        required=False,
        label='Подтверждение пароля'
    )
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'email': 'Email',
            'avatar': 'Аватар',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
    
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        
        # Если хотя бы одно поле пароля заполнено
        if any([old_password, new_password1, new_password2]):
            if not all([old_password, new_password1, new_password2]):
                raise forms.ValidationError(
                    'Для смены пароля заполните все три поля: текущий пароль, новый пароль и подтверждение.'
                )
            
            # Проверяем текущий пароль
            if not self.instance.check_password(old_password):
                raise forms.ValidationError('Неверный текущий пароль.')
            
            # Проверяем совпадение новых паролей
            if new_password1 != new_password2:
                raise forms.ValidationError('Новые пароли не совпадают.')
            
            # Валидация нового пароля
            if new_password1:
                validate_password(new_password1, self.instance)
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        
        # Если был указан новый пароль, меняем его
        new_password = self.cleaned_data.get('new_password1')
        if new_password:
            user.set_password(new_password)
        
        if commit:
            user.save()
        return user
