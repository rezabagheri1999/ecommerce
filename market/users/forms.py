from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from .models import User, UserProfile, ContactMessage
import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User

# Register
class BasicRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply form-control class to password fields
        self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder':'نام کاربری'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control','placeholder':'  رمز عبور'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control','placeholder':' تایید رمز عبور'})

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'ایمیل'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email
# Completing Register form
class ProfileCompletionForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'city', 'postal_code', 'provience']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control','placeholder':'تلفن'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,'placeholder':'آدرس'}),
            'city': forms.TextInput(attrs={'class': 'form-control','placeholder':'شهر'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control','placeholder':'کد پستی'}),
            'provience': forms.TextInput(attrs={'class': 'form-control','placeholder':'استان'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+?1?\d{9,15}$', phone_number):
            raise ValidationError("Enter a valid phone number.")
        return phone_number







#Editing Register form
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'city', 'postal_code', 'provience']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'provience': forms.TextInput(attrs={'class': 'form-control'}),
        }
# Login from
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام کاربری'
        })
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور'
        })
    )

    error_messages = {
        'invalid_login': "Invalid username or password.",
        'inactive': "This account is inactive.",
    }

# Contact form
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email','phone','subject','message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام شما'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@domain.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '09123456789'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع پیام'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'متن پیام شما...'
            }),
        }
        labels = {
            'name': 'نام کامل',
            'email': 'آدرس ایمیل',
            'phone': 'شماره تلفن (اختیاری)',
            'subject': 'موضوع پیام',
            'message': 'متن پیام',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.is_authenticated:
            self.fields['name'].initial = self.user.get_full_name() or self.user.username
            self.fields['email'].initial = self.user.email
            if hasattr(self.user, 'profile'):
                self.fields['phone'].initial = self.user.profile.phone_number

            # Make name, email, and phone readonly for logged-in users
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['phone'].widget.attrs['readonly'] = True
        else:
            # Add required attribute for non-logged-in users
            self.fields['name'].widget.attrs['required'] = 'required'
            self.fields['email'].widget.attrs['required'] = 'required'


#Reset passwordfrom django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django import forms





class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        label=False,
        widget=forms.EmailInput(attrs={

            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید',
            'autocomplete': 'email'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'پسورد جدید',
            'autocomplete': 'new-password'
        }),
        help_text="طول پسورد باید حداقل ۸ کاراکتر باشد",
    )
    new_password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تایید پسورد جدید',
            'autocomplete': 'new-password'
        }),
    )