from django.db import models

# Create your models here.

class UserRoadmap(models.Model):
    full_name = models.CharField(max_length=150)
    college = models.CharField(max_length=255)
    branch = models.CharField(max_length=150)
    current_year = models.CharField(max_length=50)
    career_interest = models.TextField()  # Stores selected interest(s), e.g. "Web Development" or comma-separated
    skill_level = models.CharField(max_length=50)
    existing_skills = models.TextField()  # Comma-separated list of skills
    learning_time = models.CharField(max_length=100)
    goal = models.CharField(max_length=150)
    
    # Store the entire generated roadmap JSON structure
    generated_roadmap = models.JSONField(default=dict)
    
    # Progress details
    progress_percentage = models.IntegerField(default=0)
    completed_topics = models.TextField(default="", blank=True)  # Comma-separated list of completed items
    learning_streak = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name}'s {self.skill_level} {self.career_interest} Roadmap"

