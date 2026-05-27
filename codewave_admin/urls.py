from django.urls import path
from . import views

app_name = 'codewave_admin'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    
    # Announcements
    path('announcements/', views.announcements_view, name='announcements_view'),
    path('announcements/add/', views.announcement_add, name='announcement_add'),
    path('announcements/edit/<int:pk>/', views.announcement_edit, name='announcement_edit'),
    path('announcements/delete/<int:pk>/', views.announcement_delete, name='announcement_delete'),
    path('announcements/pin/<int:pk>/', views.announcement_pin_toggle, name='announcement_pin_toggle'),
    
    # Events
    path('events/', views.events_view, name='events_view'),
    path('events/add/', views.event_add, name='event_add'),
    path('events/edit/<int:pk>/', views.event_edit, name='event_edit'),
    path('events/delete/<int:pk>/', views.event_delete, name='event_delete'),
    
    # Quotes
    path('quotes/', views.quotes_view, name='quotes_view'),
    path('quotes/add/', views.quote_add, name='quote_add'),
    path('quotes/edit/<int:pk>/', views.quote_edit, name='quote_edit'),
    path('quotes/delete/<int:pk>/', views.quote_delete, name='quote_delete'),
    
    # Memes
    path('memes/', views.memes_view, name='memes_view'),
    path('memes/add/', views.meme_add, name='meme_add'),
    path('memes/delete/<int:pk>/', views.meme_delete, name='meme_delete'),
    path('memes/pin/<int:pk>/', views.meme_pin_toggle, name='meme_pin_toggle'),
    
    # Users
    path('users/', views.users_view, name='users_view'),
    path('users/action/', views.user_action, name='user_action'),
    
    # Roadmaps
    path('roadmaps/', views.roadmaps_view, name='roadmaps_view'),
    path('roadmaps/delete/<int:pk>/', views.roadmap_delete, name='roadmap_delete'),
    
    # AI Settings
    path('ai-settings/', views.ai_settings_view, name='ai_settings_view'),
    
    # Analytics
    path('analytics/', views.analytics_view, name='analytics_view'),
    
    # Settings
    path('settings/', views.settings_view, name='settings_view'),
]
