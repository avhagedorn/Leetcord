from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    context = {
        "Solves" : Solve.objects.all().order_by("-date")[:15]
    }
    return render(request, "Data/index.html", context=context)

def solution(request,id):
    solves = Solve.objects.filter(pk=id).first()
    if solves:
        context = {
            "solve" : solves,
            "ProblemSolves":solves.problem.Solves.all().order_by("-date")[:15]
        }
    else:
        context = {
            "id" : id
        }
    return render(request, "Data/solution.html",context=context)