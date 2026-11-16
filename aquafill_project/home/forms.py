from django import forms
from .models import RefillReport, WaterStation

INPUT_CLASSES = (
    'w-full px-4 py-2.5 rounded-lg border border-slate-300 '
    'bg-white text-slate-800 placeholder-slate-400 '
    'focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500 '
    'transition duration-150 text-sm'
)


class RefillReportForm(forms.ModelForm):
    class Meta:
        model = RefillReport
        fields = ('station', 'issue_type', 'notes')
        widgets = {
            'station': forms.Select(attrs={'class': INPUT_CLASSES}),
            'issue_type': forms.Select(attrs={'class': INPUT_CLASSES}),
            'notes': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 3, 'placeholder': 'Describe what needs attention (e.g. Tank completely empty since morning)'}),
        }
