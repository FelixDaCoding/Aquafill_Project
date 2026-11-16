from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import Profile

TEXT_INPUT_CLASSES = (
    'w-full px-4 py-3 rounded-lg border border-slate-300 '
    'bg-white text-slate-800 placeholder-slate-400 '
    'focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500 '
    'transition duration-150'
)


class AquaFillLoginForm(AuthenticationForm):
    """Login form for existing AquaFill users (students, faculty, staff)."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': TEXT_INPUT_CLASSES,
            'placeholder': 'Enter your username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': TEXT_INPUT_CLASSES,
            'placeholder': 'Enter your password',
        })
    )


class AquaFillRegisterForm(UserCreationForm):
    """
    Registration form collecting Username, Institutional Email, Role,
    Password, and Confirm Password, then creating a User + linked Profile atomically.
    """

    institutional_email = forms.EmailField(
        required=True,
        label='Institutional Email',
        widget=forms.EmailInput(attrs={
            'class': TEXT_INPUT_CLASSES,
            'placeholder': 'you@university.edu.ph',
        })
    )
    role = forms.ChoiceField(
        choices=Profile.Role.choices,
        required=True,
        label='Role',
        widget=forms.Select(attrs={'class': TEXT_INPUT_CLASSES})
    )

    class Meta:
        model = User
        fields = ('username', 'institutional_email', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': TEXT_INPUT_CLASSES,
            'placeholder': 'Choose a username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': TEXT_INPUT_CLASSES,
            'placeholder': 'Create a password',
        })
        self.fields['password1'].label = 'Password'
        self.fields['password2'].widget.attrs.update({
            'class': TEXT_INPUT_CLASSES,
            'placeholder': 'Re-enter your password',
        })
        self.fields['password2'].label = 'Confirm Password'

    def clean_institutional_email(self):
        email = self.cleaned_data.get('institutional_email', '').strip().lower()
        if Profile.objects.filter(institutional_email=email).exists():
            raise forms.ValidationError('This institutional email is already registered.')
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['institutional_email']
        user.email = email
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                institutional_email=email,
                role=self.cleaned_data['role'],
            )
        return user
