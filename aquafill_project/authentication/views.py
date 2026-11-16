from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .forms import AquaFillLoginForm, AquaFillRegisterForm


class AquaFillLoginView(LoginView):
    """Handles authentication and redirects straight to /home/ on success."""
    template_name = 'authentication/login.html'
    authentication_form = AquaFillLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home:home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class AquaFillRegisterView(View):
    """Handles new account creation for Students, Faculty, and Facility Staff."""
    template_name = 'authentication/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = AquaFillRegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AquaFillRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to AquaFill, {user.username}! Your account was created successfully.')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


def aquafill_logout_view(request):
    """Logs current user out (accepts both POST for security and GET with redirect)."""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
    return redirect('authentication:login')
