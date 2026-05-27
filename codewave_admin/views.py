from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from waves.models import UserRoadmap
from .models import Announcement, Event, DeveloperQuote, Meme, SystemSetting, ActivityLog
import json

# Decorator to ensure only admin/staff access the dashboard
def admin_only(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='codewave_admin:admin_login'
    )
    return actual_decorator(view_func)

def log_activity(user, action, details=""):
    ActivityLog.objects.create(user=user, action=action, details=details)

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('codewave_admin:admin_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                auth_login(request, user)
                log_activity(user, "Admin Logged In", "Successfully authenticated into admin dashboard.")
                return redirect('codewave_admin:admin_dashboard')
            else:
                messages.error(request, "Access denied. Admin access only.")
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'codewave_admin/login.html')

def admin_logout(request):
    if request.user.is_authenticated:
        log_activity(request.user, "Admin Logged Out", "User logged out of admin session.")
        auth_logout(request)
    return redirect('codewave_admin:admin_login')

@admin_only
def admin_dashboard(request):
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_roadmaps = UserRoadmap.objects.count()
    total_events = Event.objects.count()
    
    # AI usage setting count
    ai_usage_setting, _ = SystemSetting.objects.get_or_create(
        key='ai_usage_count', 
        defaults={'value': '142', 'description': 'Total count of AI roadmap compilations'}
    )
    ai_usage_count = int(ai_usage_setting.value)
    
    # Community growth (simulated/calculated)
    growth = "12%"
    
    # Recent logs
    logs = ActivityLog.objects.all()[:10]
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_roadmaps': total_roadmaps,
        'total_events': total_events,
        'ai_usage_count': ai_usage_count,
        'growth': growth,
        'activity_logs': logs,
        'active_tab': 'dashboard'
    }
    return render(request, 'codewave_admin/dashboard.html', context)

@admin_only
def announcements_view(request):
    announcements = Announcement.objects.all()
    context = {
        'announcements': announcements,
        'active_tab': 'announcements'
    }
    return render(request, 'codewave_admin/announcements.html', context)

@admin_only
def announcement_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority', 'low')
        publish_date = request.POST.get('publish_date') or timezone.now().date()
        is_pinned = request.POST.get('is_pinned') == 'on'
        
        image = None
        if 'image' in request.FILES:
            image = request.FILES['image']
            
        announcement = Announcement.objects.create(
            title=title,
            description=description,
            priority=priority,
            publish_date=publish_date,
            is_pinned=is_pinned,
            image=image
        )
        log_activity(request.user, "Added Announcement", f"Created announcement ID {announcement.id}: {title}")
        messages.success(request, "Announcement added successfully!")
    return redirect('codewave_admin:announcements_view')

@admin_only
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.title = request.POST.get('title')
        announcement.description = request.POST.get('description')
        announcement.priority = request.POST.get('priority', 'low')
        if request.POST.get('publish_date'):
            announcement.publish_date = request.POST.get('publish_date')
        announcement.is_pinned = request.POST.get('is_pinned') == 'on'
        
        if 'image' in request.FILES:
            announcement.image = request.FILES['image']
            
        announcement.save()
        log_activity(request.user, "Edited Announcement", f"Updated announcement ID {announcement.id}")
        messages.success(request, "Announcement updated successfully!")
    return redirect('codewave_admin:announcements_view')

@admin_only
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    title = announcement.title
    announcement.delete()
    log_activity(request.user, "Deleted Announcement", f"Removed announcement ID {pk}: {title}")
    messages.success(request, "Announcement deleted successfully!")
    return redirect('codewave_admin:announcements_view')

@admin_only
def announcement_pin_toggle(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.is_pinned = not announcement.is_pinned
    announcement.save()
    status = "Pinned" if announcement.is_pinned else "Unpinned"
    log_activity(request.user, f"{status} Announcement", f"Toggled pinned state of announcement ID {pk}")
    messages.success(request, f"Announcement successfully {status.lower()}!")
    return redirect('codewave_admin:announcements_view')

@admin_only
def events_view(request):
    events = Event.objects.all()
    context = {
        'events': events,
        'active_tab': 'events'
    }
    return render(request, 'codewave_admin/events.html', context)

@admin_only
def event_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date') or timezone.now().date()
        time = request.POST.get('time') or timezone.now().time()
        meeting_link = request.POST.get('meeting_link')
        speaker_name = request.POST.get('speaker_name')
        
        banner = None
        if 'banner' in request.FILES:
            banner = request.FILES['banner']
            
        event = Event.objects.create(
            name=name,
            description=description,
            date=date,
            time=time,
            meeting_link=meeting_link,
            speaker_name=speaker_name,
            banner=banner
        )
        log_activity(request.user, "Created Event", f"Created event ID {event.id}: {name}")
        messages.success(request, "Event created successfully!")
    return redirect('codewave_admin:events_view')

@admin_only
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.name = request.POST.get('name')
        event.description = request.POST.get('description')
        if request.POST.get('date'):
            event.date = request.POST.get('date')
        if request.POST.get('time'):
            event.time = request.POST.get('time')
        event.meeting_link = request.POST.get('meeting_link')
        event.speaker_name = request.POST.get('speaker_name')
        
        if 'banner' in request.FILES:
            event.banner = request.FILES['banner']
            
        event.save()
        log_activity(request.user, "Edited Event", f"Updated event ID {event.id}")
        messages.success(request, "Event updated successfully!")
    return redirect('codewave_admin:events_view')

@admin_only
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    name = event.name
    event.delete()
    log_activity(request.user, "Deleted Event", f"Removed event ID {pk}: {name}")
    messages.success(request, "Event deleted successfully!")
    return redirect('codewave_admin:events_view')

@admin_only
def quotes_view(request):
    quotes = DeveloperQuote.objects.all()
    context = {
        'quotes': quotes,
        'active_tab': 'quotes'
    }
    return render(request, 'codewave_admin/quotes.html', context)

@admin_only
def quote_add(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        author_name = request.POST.get('author_name')
        
        author_image = None
        if 'author_image' in request.FILES:
            author_image = request.FILES['author_image']
            
        quote = DeveloperQuote.objects.create(
            text=text,
            author_name=author_name,
            author_image=author_image
        )
        log_activity(request.user, "Added Developer Quote", f"Created quote ID {quote.id} by {author_name}")
        messages.success(request, "Quote added successfully!")
    return redirect('codewave_admin:quotes_view')

@admin_only
def quote_edit(request, pk):
    quote = get_object_or_404(DeveloperQuote, pk=pk)
    if request.method == 'POST':
        quote.text = request.POST.get('text')
        quote.author_name = request.POST.get('author_name')
        
        if 'author_image' in request.FILES:
            quote.author_image = request.FILES['author_image']
            
        quote.save()
        log_activity(request.user, "Edited Developer Quote", f"Updated quote ID {quote.id}")
        messages.success(request, "Quote updated successfully!")
    return redirect('codewave_admin:quotes_view')

@admin_only
def quote_delete(request, pk):
    quote = get_object_or_404(DeveloperQuote, pk=pk)
    author = quote.author_name
    quote.delete()
    log_activity(request.user, "Deleted Developer Quote", f"Removed quote ID {pk} by {author}")
    messages.success(request, "Quote deleted successfully!")
    return redirect('codewave_admin:quotes_view')

@admin_only
def memes_view(request):
    memes = Meme.objects.all()
    context = {
        'memes': memes,
        'active_tab': 'memes'
    }
    return render(request, 'codewave_admin/memes.html', context)

@admin_only
def meme_add(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        tags = request.POST.get('tags')
        is_pinned = request.POST.get('is_pinned') == 'on'
        
        if 'image' in request.FILES:
            image = request.FILES['image']
            meme = Meme.objects.create(
                image=image,
                caption=caption,
                tags=tags,
                is_pinned=is_pinned
            )
            log_activity(request.user, "Added Meme", f"Created meme ID {meme.id}: {caption}")
            messages.success(request, "Meme uploaded successfully!")
        else:
            messages.error(request, "Meme image is required.")
    return redirect('codewave_admin:memes_view')

@admin_only
def meme_delete(request, pk):
    meme = get_object_or_404(Meme, pk=pk)
    meme.delete()
    log_activity(request.user, "Deleted Meme", f"Removed meme ID {pk}")
    messages.success(request, "Meme deleted successfully!")
    return redirect('codewave_admin:memes_view')

@admin_only
def meme_pin_toggle(request, pk):
    meme = get_object_or_404(Meme, pk=pk)
    meme.is_pinned = not meme.is_pinned
    meme.save()
    status = "Pinned" if meme.is_pinned else "Unpinned"
    log_activity(request.user, f"{status} Meme", f"Toggled pinned state of meme ID {pk}")
    messages.success(request, f"Meme successfully {status.lower()}!")
    return redirect('codewave_admin:memes_view')

@admin_only
def users_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        users = User.objects.filter(
            models.Q(username__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query)
        )
    else:
        users = User.objects.all()
        
    context = {
        'users': users,
        'search_query': search_query,
        'active_tab': 'users'
    }
    return render(request, 'codewave_admin/users.html', context)

@admin_only
def user_action(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user_obj = get_object_or_404(User, id=user_id)
        
        if action == 'ban':
            user_obj.is_active = False
            user_obj.save()
            log_activity(request.user, "Banned User", f"Deactivated user ID {user_id}: {user_obj.username}")
            messages.success(request, f"User {user_obj.username} has been banned.")
            
        elif action == 'suspend':
            user_obj.is_active = False
            user_obj.save()
            log_activity(request.user, "Suspended User", f"Suspended account for user ID {user_id}: {user_obj.username}")
            messages.success(request, f"User {user_obj.username}'s account suspended.")
            
        elif action == 'activate':
            user_obj.is_active = True
            user_obj.save()
            log_activity(request.user, "Activated User", f"Re-activated user ID {user_id}: {user_obj.username}")
            messages.success(request, f"User {user_obj.username} activated.")
            
        elif action == 'change_role':
            new_role = request.POST.get('role')
            if new_role == 'admin':
                user_obj.is_staff = True
            else:
                user_obj.is_staff = False
            user_obj.save()
            log_activity(request.user, "Changed User Role", f"Updated user ID {user_id} staff status to {user_obj.is_staff}")
            messages.success(request, f"Role updated for {user_obj.username}.")
            
        elif action == 'reset_password':
            new_pwd = request.POST.get('new_password')
            if new_pwd:
                user_obj.set_password(new_pwd)
                user_obj.save()
                log_activity(request.user, "Reset User Password", f"Forced password change on user ID {user_id}")
                messages.success(request, f"Password reset for {user_obj.username} successfully.")
            else:
                messages.error(request, "Password cannot be blank.")
                
    return redirect('codewave_admin:users_view')

@admin_only
def roadmaps_view(request):
    roadmaps = UserRoadmap.objects.order_by('-created_at') if hasattr(UserRoadmap, 'created_at') else UserRoadmap.objects.all()
    
    # Categories / resources templates config from SystemSettings
    roadmap_template_setting, _ = SystemSetting.objects.get_or_create(
        key='ai_roadmap_templates',
        defaults={'value': '{"Web Development": "Standard 90-day frontend path with HTML/CSS/JS and React.", "AI / Machine Learning": "Core ML pathway using Python, Jupyter, NumPy, Pandas, Scikit-Learn."}', 'description': 'AI templates config JSON'}
    )
    
    context = {
        'roadmaps': roadmaps,
        'ai_templates': json.loads(roadmap_template_setting.value),
        'active_tab': 'roadmaps'
    }
    return render(request, 'codewave_admin/roadmaps.html', context)

@admin_only
def roadmap_delete(request, pk):
    roadmap = get_object_or_404(UserRoadmap, pk=pk)
    owner = roadmap.full_name
    roadmap.delete()
    log_activity(request.user, "Deleted Roadmap", f"Removed generated roadmap ID {pk} for {owner}")
    messages.success(request, "Roadmap deleted successfully!")
    return redirect('codewave_admin:roadmaps_view')

@admin_only
def ai_settings_view(request):
    # Prompt template, behaviour settings
    prompt_temp, _ = SystemSetting.objects.get_or_create(
        key='ai_prompt_template',
        defaults={'value': 'You are an advanced learning counselor. Design a step-by-step roadmap for a student named {fullName} studying in {college} year {currentYear}...', 'description': 'Base prompt for roadmap generation'}
    )
    chatbot_greeting, _ = SystemSetting.objects.get_or_create(
        key='chatbot_greeting',
        defaults={'value': 'Hello! I am WaveBot. Ask me anything about programming or your roadmap.', 'description': 'Greeting sentence for chat'}
    )
    model_temp, _ = SystemSetting.objects.get_or_create(
        key='ai_temperature',
        defaults={'value': '0.7', 'description': 'Temperature factor of AI model outputs'}
    )
    
    if request.method == 'POST':
        prompt_temp.value = request.POST.get('prompt_template')
        prompt_temp.save()
        
        chatbot_greeting.value = request.POST.get('chatbot_greeting')
        chatbot_greeting.save()
        
        model_temp.value = request.POST.get('ai_temperature')
        model_temp.save()
        
        log_activity(request.user, "Updated AI Settings", "Modified system prompt templates and models values.")
        messages.success(request, "AI configuration saved successfully!")
        
    context = {
        'prompt_template': prompt_temp.value,
        'chatbot_greeting': chatbot_greeting.value,
        'ai_temperature': model_temp.value,
        'active_tab': 'ai-settings'
    }
    return render(request, 'codewave_admin/ai_settings.html', context)

@admin_only
def analytics_view(request):
    # Analytics data: counts per interest, skill level distributions, active growth
    # We pass pre-calculated variables to generate neat Chart.js canvas elements
    interests = ['Web Development', 'AI / Machine Learning', 'Data Science', 'Cyber Security', 'App Development']
    interest_counts = []
    for category in interests:
        count = UserRoadmap.objects.filter(career_interest__icontains=category).count()
        interest_counts.append(count)
        
    skill_beginner = UserRoadmap.objects.filter(skill_level__iexact='beginner').count()
    skill_intermediate = UserRoadmap.objects.filter(skill_level__iexact='intermediate').count()
    skill_advanced = UserRoadmap.objects.filter(skill_level__iexact='advanced').count()
    
    context = {
        'interests_labels': json.dumps(interests),
        'interests_data': json.dumps(interest_counts),
        'skills_data': json.dumps([skill_beginner, skill_intermediate, skill_advanced]),
        'active_tab': 'analytics'
    }
    return render(request, 'codewave_admin/analytics.html', context)

@admin_only
def settings_view(request):
    logo, _ = SystemSetting.objects.get_or_create(
        key='site_logo',
        defaults={'value': '🌊 CODEWAVE', 'description': 'Logo string or path'}
    )
    theme, _ = SystemSetting.objects.get_or_create(
        key='site_theme',
        defaults={'value': 'cyberpunk-dark', 'description': 'UI Theme configuration'}
    )
    social_github, _ = SystemSetting.objects.get_or_create(
        key='social_github',
        defaults={'value': 'https://github.com', 'description': 'GitHub link'}
    )
    social_discord, _ = SystemSetting.objects.get_or_create(
        key='social_discord',
        defaults={'value': 'https://discord.com', 'description': 'Discord channel link'}
    )
    navbar_visible, _ = SystemSetting.objects.get_or_create(
        key='navbar_visible',
        defaults={'value': 'true', 'description': 'Show community navbar links'}
    )
    
    if request.method == 'POST':
        logo.value = request.POST.get('site_logo')
        logo.save()
        theme.value = request.POST.get('site_theme')
        theme.save()
        social_github.value = request.POST.get('social_github')
        social_github.save()
        social_discord.value = request.POST.get('social_discord')
        social_discord.save()
        navbar_visible.value = 'true' if request.POST.get('navbar_visible') == 'on' else 'false'
        navbar_visible.save()
        
        log_activity(request.user, "Updated Dashboard Settings", "Modified general site styling configurations.")
        messages.success(request, "Global system configurations saved successfully!")
        
    context = {
        'site_logo': logo.value,
        'site_theme': theme.value,
        'social_github': social_github.value,
        'social_discord': social_discord.value,
        'navbar_visible': navbar_visible.value == 'true',
        'active_tab': 'settings'
    }
    return render(request, 'codewave_admin/settings.html', context)
