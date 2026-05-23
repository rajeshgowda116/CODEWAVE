from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserRoadmap
import json

# Create your views here.
def codelogin(request):
    if request.method == 'POST':
      code=request.POST.get('input-text')
      if code=='C2O0D2E6':
        return redirect('main')
      else:
        return redirect('code_error') 
    return render(request,"input.html")

def main(request):
    return render(request,"main.html")

def code_error(request):
    return render(request,"zany_emoji.html")

def roadmap(request):
    roadmap_id = request.GET.get('id')
    context = {}
    if roadmap_id:
        try:
            roadmap_obj = UserRoadmap.objects.get(id=roadmap_id)
            context['loaded_roadmap_id'] = roadmap_obj.id
            context['loaded_roadmap_name'] = roadmap_obj.full_name
        except UserRoadmap.DoesNotExist:
            pass
    return render(request, "roadmap.html", context)

@csrf_exempt
def save_roadmap_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            roadmap_id = data.get('id')
            
            if roadmap_id:
                # Update existing roadmap
                roadmap_obj = get_object_or_404(UserRoadmap, id=roadmap_id)
            else:
                # Create a new roadmap
                roadmap_obj = UserRoadmap()
                
            roadmap_obj.full_name = data.get('full_name', '')
            roadmap_obj.college = data.get('college', '')
            roadmap_obj.branch = data.get('branch', '')
            roadmap_obj.current_year = data.get('current_year', '')
            roadmap_obj.career_interest = data.get('career_interest', '')
            roadmap_obj.skill_level = data.get('skill_level', '')
            roadmap_obj.existing_skills = data.get('existing_skills', '')
            roadmap_obj.learning_time = data.get('learning_time', '')
            roadmap_obj.goal = data.get('goal', '')
            roadmap_obj.generated_roadmap = data.get('generated_roadmap', {})
            roadmap_obj.progress_percentage = int(data.get('progress_percentage', 0))
            roadmap_obj.completed_topics = data.get('completed_topics', '')
            roadmap_obj.learning_streak = int(data.get('learning_streak', 0))
            
            roadmap_obj.save()
            return JsonResponse({'status': 'success', 'id': roadmap_obj.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)

def load_roadmap_api(request, roadmap_id):
    roadmap_obj = get_object_or_404(UserRoadmap, id=roadmap_id)
    data = {
        'id': roadmap_obj.id,
        'full_name': roadmap_obj.full_name,
        'college': roadmap_obj.college,
        'branch': roadmap_obj.branch,
        'current_year': roadmap_obj.current_year,
        'career_interest': roadmap_obj.career_interest,
        'skill_level': roadmap_obj.skill_level,
        'existing_skills': roadmap_obj.existing_skills,
        'learning_time': roadmap_obj.learning_time,
        'goal': roadmap_obj.goal,
        'generated_roadmap': roadmap_obj.generated_roadmap,
        'progress_percentage': roadmap_obj.progress_percentage,
        'completed_topics': roadmap_obj.completed_topics,
        'learning_streak': roadmap_obj.learning_streak,
        'created_at': roadmap_obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    return JsonResponse({'status': 'success', 'data': data})
