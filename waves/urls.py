from django.urls import path
from . import views

urlpatterns = [
    path('codelogin/',views.codelogin,name='codelogin'),
    path('main/',views.main,name='main'),
    path('code_error/',views.code_error,name='code_error'), 
    path('login/',views.login_view,name='login'), 
]