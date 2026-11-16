from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import StyledPasswordChangeForm, UserSettingsPreferencesForm
from .models import UserSettings


@login_required
def settings_view(request):
    """Unified settings view for application preferences and password changes."""
    user_settings, _ = UserSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_preferences':
            form = UserSettingsPreferencesForm(request.POST, instance=user_settings)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your notification and dashboard preferences have been saved!')
                return redirect('user_settings:settings')
            password_form = StyledPasswordChangeForm(user=request.user)

        elif action == 'change_password':
            password_form = StyledPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, 'Your password was successfully updated!')
                return redirect('user_settings:settings')
            else:
                messages.error(request, 'Please correct the errors below to update your password.')
            form = UserSettingsPreferencesForm(instance=user_settings)
        else:
            form = UserSettingsPreferencesForm(instance=user_settings)
            password_form = StyledPasswordChangeForm(user=request.user)
    else:
        form = UserSettingsPreferencesForm(instance=user_settings)
        password_form = StyledPasswordChangeForm(user=request.user)

    context = {
        'preferences_form': form,
        'password_form': password_form,
        'user_settings': user_settings,
    }
    return render(request, 'user_settings/settings.html', context)
