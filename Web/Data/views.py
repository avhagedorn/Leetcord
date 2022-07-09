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

def member(request, discord_id):
    user = Member.objects.filter(discordID=discord_id).first()
    if user:
        context = {
            "user" : user,
            "userSolves" : user.Solves.all().order_by("-date")[:15]
        }
    else:
        context = {
            "discordID" : discord_id
        }
    return render(request, "Data/member.html", context=context)