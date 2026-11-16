from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('edit/', views.profile_edit_view, name='edit'),
    path('log-water/', views.log_hydration_view, name='log_water'),
]
