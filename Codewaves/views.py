from django.shortcuts import render,redirect

# Create your views here.
# Start with here
def index(request):
    return render(request,"index.html")