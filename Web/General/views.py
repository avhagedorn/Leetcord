from django.shortcuts import render

# Create your views here.

def about(request):
    return render(request,"General/about.html")

def commands(request):
    return render(request,"General/commands.html")