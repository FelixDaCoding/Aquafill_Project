from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('report/', views.report_station_view, name='report'),
    path('refill/<int:station_id>/', views.refill_station_action, name='refill'),
]
