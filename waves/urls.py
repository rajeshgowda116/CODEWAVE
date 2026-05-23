from django.urls import path
from . import views

urlpatterns = [
    path('codelogin/',views.codelogin,name='codelogin'),
    path('main/',views.main,name='main'),
    path('code_error/',views.code_error,name='code_error'), 
    path('roadmap/', views.roadmap, name='roadmap'),
    path('api/roadmap/save/', views.save_roadmap_api, name='save_roadmap_api'),
    path('api/roadmap/load/<int:roadmap_id>/', views.load_roadmap_api, name='load_roadmap_api'),
]