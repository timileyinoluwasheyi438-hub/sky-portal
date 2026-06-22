from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teams/', views.team_list, name='team_list'),
    path('teams/create/', views.team_create, name='team_create'),
    path('teams/<int:pk>/', views.team_detail, name='team_detail'),
    path('teams/<int:pk>/edit/', views.team_edit, name='team_edit'),
    path('teams/<int:pk>/disband/', views.team_disband, name='team_disband'),
    path('search/', views.search, name='search'),
    path('audit/', views.audit_log, name='audit_log'),
]