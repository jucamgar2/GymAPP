from django import forms
from .models import CustomUser

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    age = forms.IntegerField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya existe')
        if len(username) < 5:
            raise forms.ValidationError('El nombre de usuario debe tener al menos 5 caracteres')
        if len(username) > 20:
            raise forms.ValidationError('El nombre de usuario no puede tener más de 20 caracteres')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 4:
            raise forms.ValidationError('La contraseña debe tener al menos 4 caracteres')
        if len(password) > 20:
            raise forms.ValidationError('La contraseña no puede tener más de 20 caracteres')
        return password
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya existe')
        if len(email) > 50:
            raise forms.ValidationError('El email no puede tener más de 50 caracteres')
        return email
    
    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 14:
            raise forms.ValidationError('Debes tener al menos 14 años para usar la aplicación')
        if age > 150:
            raise forms.ValidationError('La edad no puede ser mayor a 150')
        return age