from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Address, CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    # Model field is `phone`, not `phone_number`
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Use email as username since login is email-based
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # Model field is `phone`, not `phone_number`
        fields = ('first_name', 'last_name', 'phone')


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        # Model fields: full_name, phone, city, street, is_default
        # (no street_address / state / postal_code / country in the model)
        fields = ('full_name', 'phone', 'city', 'street', 'is_default')


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user_obj = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError('Invalid email or password.')

            user = authenticate(username=user_obj.username, password=password)
            if user is None:
                raise forms.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise forms.ValidationError('This account is inactive.')

            self._user = user

        return cleaned_data

    def get_user(self):
        return self._user
