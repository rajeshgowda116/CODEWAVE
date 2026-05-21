from django.shortcuts import render,redirect

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

def login_view(request):
    if request.method == 'POST':
        # For demonstration or simple flow, redirect to main on post submit
        return redirect('main')
    return render(request, "login.html")





