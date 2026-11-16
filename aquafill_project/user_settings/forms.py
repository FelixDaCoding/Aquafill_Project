from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserSettings


class UserSettingsPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = (
            'email_station_alerts',
            'low_water_notifications',
            'dark_mode_preference',
            'auto_refresh_dashboard',
            'show_hydration_reminder',
        )
        widgets = {
            'email_station_alerts': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-teal-600 rounded border-slate-300 focus:ring-teal-500'}),
            'low_water_notifications': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-teal-600 rounded border-slate-300 focus:ring-teal-500'}),
            'dark_mode_preference': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-teal-600 rounded border-slate-300 focus:ring-teal-500'}),
            'auto_refresh_dashboard': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-teal-600 rounded border-slate-300 focus:ring-teal-500'}),
            'show_hydration_reminder': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-teal-600 rounded border-slate-300 focus:ring-teal-500'}),
        }


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_classes = (
            'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
            'bg-white text-slate-800 placeholder-slate-400 '
            'focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500 '
            'transition duration-150 text-sm'
        )
        for field in self.fields.values():
            field.widget.attrs.update({'class': input_classes})
