from django.urls import path

from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.AquaFillLoginView.as_view(), name='login'),
    path('register/', views.AquaFillRegisterView.as_view(), name='register'),
    path('logout/', views.aquafill_logout_view, name='logout'),
]
