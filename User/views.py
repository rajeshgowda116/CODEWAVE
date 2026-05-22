from django.shortcuts import render, redirect

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        # For demonstration or simple flow, redirect to main on post submit
        return redirect('main')
    return render(request, "login.html")


def register_view(request):
    if request.method == 'POST':
        # For demonstration or simple flow, redirect to login page after submit
        return redirect('login')
    return render(request, "registration.html")
