from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    context = {
        "Solves" : Solve.objects.all().order_by("-date")[:15]
    }
    return render(request, "Data/index.html", context=context)