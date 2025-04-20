from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol kamida 8 ta belgi'}),
        label='Parol'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni tasdiqlash'}),
        label='Parol'
    )
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        }
         
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('Parollar mos emas')
        return password2

    def save(self, commit=True):  
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # ✅ Parolni hash qilib saqlash
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    user_or_phone = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'})
    )

    def clean(self):
        cleaned_data = super().clean()
        user_or_phone = cleaned_data.get('user_or_phone')
        password = cleaned_data.get('password')

        user = User.objects.filter(username=user_or_phone).first()
        if not user:
            raise forms.ValidationError("Bunday foydalanuvchi topilmadi!")

        # ✅ `authenticate()` orqali parolni tekshirish
        user = authenticate(username=user.username, password=password)
        if not user:
            raise forms.ValidationError("Noto‘g‘ri parol!")

        self.user = user
        return cleaned_data

    def get_user(self):
        return self.user
    
    
class UserProfileForm(forms.ModelForm):
    username = forms.EmailField(required=False)  # Email maydoni qo‘shildi

    phone_regex = RegexValidator(
        regex=r'^\+998[0-9]{9}$',
        message="Telefon raqami +998 bilan boshlanib, keyin 9 ta raqam bo'lishi kerak."
    )
    
    class Meta:
        model = ProfileUser
        fields = ['role','full_name', 'workplace','department','faculty','university','specialization','grade', 'phone_number','birthdate','username','profile_pic']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ism, Familiya va Sharif'}),
            'workplace': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ish joyi'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fakultet'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kafedra'}),
            'university': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "O'qish joyi"}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Yo'nalish"}),
            'grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guruh'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998-00-000-00-00'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username  # Username ni formaga chiqarish

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user  # User obyektini olish
        new_username = self.cleaned_data.get('username')  # Foydalanuvchi kiritgan email (username)

        if new_username and new_username != user.username:
            user.username = new_username  # Username yangilash
            user.email = new_username  # Emailni ham yangilash
            user.save()  # User modelini saqlash

        profile.save()  # Profile modelini saqlash
        return profile
        
        
class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        max_length=13,
        widget = forms.TextInput(attrs={'placeholder': 'Telefon raqmingiz', 'class': 'form-control'}),
        label = "Telefon raqam"
    )
    
class VerificationCodeForm(forms.Form):
    code = forms.CharField(
        max_length=4,
        widget = forms.TextInput(attrs={'placeholder': 'Tasqidlash kodini kiriting', 'class': 'form-control'}),
        label = "Tasdiqlash kodi"
    )
    
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget = forms.PasswordInput(attrs={'placeholder': 'Yangi parol', 'class': 'form-control'}),
        label = "Yangi parol"
    )
    
    confirm_password = forms.CharField(
        widget = forms.PasswordInput(attrs={'placeholder': 'Parolni takrorlang', 'class': 'form-control'}),
        label = "Parolni takrorlang"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError("Parollar mos emas.")
        return cleaned_data
    
    
class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)

        for question in questions:
            choices = [
                ('a', question.a_javob),
                ('b', question.b_javob),
                ('c', question.c_javob),
                ('d', question.d_javob),
            ]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices, widget=forms.RadioSelect, label=question.savol, required=True
            )
    
    

