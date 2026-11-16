from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import HydrationLogForm, UserBasicInfoForm, UserProfileDetailsForm
from .models import UserProfile


@login_required
def profile_view(request):
    """Displays user profile, campus affiliation, role, and hydration metrics."""
    profile_details, _ = UserProfile.objects.get_or_create(user=request.user)
    campus_profile = getattr(request.user, 'profile', None)

    hydration_form = HydrationLogForm()

    context = {
        'profile_details': profile_details,
        'campus_profile': campus_profile,
        'hydration_form': hydration_form,
    }
    return render(request, 'user_profile/profile.html', context)


@login_required
def profile_edit_view(request):
    """Allows user to update personal info, student ID, bio, and hydration goals."""
    profile_details, _ = UserProfile.objects.get_or_create(user=request.user)
    campus_profile = getattr(request.user, 'profile', None)

    if request.method == 'POST':
        user_form = UserBasicInfoForm(request.POST, instance=request.user)
        details_form = UserProfileDetailsForm(request.POST, instance=profile_details)

        if user_form.is_valid() and details_form.is_valid():
            user_form.save()
            details_form.save()
            messages.success(request, 'Your profile has been successfully updated!')
            return redirect('user_profile:profile')
    else:
        user_form = UserBasicInfoForm(instance=request.user)
        details_form = UserProfileDetailsForm(instance=profile_details)

    context = {
        'user_form': user_form,
        'details_form': details_form,
        'campus_profile': campus_profile,
    }
    return render(request, 'user_profile/profile_edit.html', context)


@login_required
def log_hydration_view(request):
    """Quick action to log water intake for the day."""
    if request.method == 'POST':
        form = HydrationLogForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount_ml']
            profile_details, _ = UserProfile.objects.get_or_create(user=request.user)
            profile_details.water_consumed_today_ml += amount
            profile_details.save()
            messages.success(request, f'Logged +{amount} ml of water! Stay hydrated! 💧')
    return redirect('user_profile:profile')
