from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Announcement(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='announcements/', blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    publish_date = models.DateField(default=timezone.now)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_pinned', '-publish_date', '-created_at']

    def __str__(self):
        return self.title

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    banner = models.ImageField(upload_to='events/', blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True)
    speaker_name = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return self.name

class DeveloperQuote(models.Model):
    text = models.TextField()
    author_name = models.CharField(max_length=150)
    author_image = models.ImageField(upload_to='quotes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.text[:50]}..." - {self.author_name}'

class Meme(models.Model):
    image = models.ImageField(upload_to='memes/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, null=True, help_text="Comma-separated tags")
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.caption or f"Meme {self.id}"

class SystemSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.key

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action} @ {self.timestamp}"
