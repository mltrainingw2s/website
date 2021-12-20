from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")

def imgdetect(request):
    return render(request,"imagedetect.html")

def videodetect(request):
    return render(request,"webcamdetect.html")