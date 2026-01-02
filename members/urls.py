"""
URL Configuration for Members App
"""
from django.urls import path
from . import views

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    
    # Member views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sign-documents/', views.sign_documents, name='sign_documents'),
    path('checkin/', views.checkin, name='checkin'),
    path('goals/', views.goals, name='goals'),
    path('profile/', views.profile, name='profile'),
    
    # Staff views
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/members/', views.staff_members, name='staff_members'),
    path('staff/members/<uuid:member_id>/', views.staff_member_detail, name='staff_member_detail'),
    path('staff/members/<uuid:member_id>/approve/', views.staff_approve_member, name='staff_approve_member'),
    path('staff/checkins/', views.staff_checkins, name='staff_checkins'),
    path('staff/checkins/<uuid:checkin_id>/approve/', views.staff_approve_checkin, name='staff_approve_checkin'),
]
