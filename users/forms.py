from django import forms
from django.contrib.auth import get_user_model


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input__log'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input__log'}))


class RegistrationUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин',  widget=forms.TextInput(attrs={'class': 'form-input__reg'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input__reg'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-input__reg'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input__reg'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input__reg'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input__reg'})
        }
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой e-mail уже зарегистрирован')
        return email
