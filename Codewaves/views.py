from django.shortcuts import render

# Create your views here.
# Start with here

def index(request):
    return render(request, "codewave.html")


def custom_404(request, exception):
    # Uses template/404.html
    return render(request, "404.html", status=404)


