from django import forms
from django.contrib.auth.models import User
from authentication.models import Profile
# pyrefly: ignore [missing-import]
from .models import UserProfile

INPUT_CLASSES = (
    'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
    'bg-white text-slate-800 placeholder-slate-400 '
    'focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500 '
    'transition duration-150 text-sm'
)


class UserBasicInfoForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Primary Email'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserProfileDetailsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('department', 'student_id', 'phone_number', 'bio', 'daily_water_target_ml')
        widgets = {
            'department': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. College of Computer Studies'}),
            'student_id': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. 21-1234-567'}),
            'phone_number': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. +63 912 345 6789'}),
            'bio': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'daily_water_target_ml': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'min': 500, 'max': 10000, 'step': 100}),
        }


class HydrationLogForm(forms.Form):
    amount_ml = forms.IntegerField(
        min_value=50,
        max_value=2000,
        initial=250,
        widget=forms.NumberInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Amount in ml (e.g. 250, 500)'
        })
    )
