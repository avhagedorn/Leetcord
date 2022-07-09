from django.shortcuts import redirect, render
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
            "member" : user,
            "userSolves" : user.Solves.all().order_by("-date")[:15]
        }
    else:
        context = {
            "discordID" : discord_id
        }
    return render(request, "Data/member.html", context=context)

def postProblem(request):
    if request.POST and request.POST.get('LCNum'):
        return redirect('Data:problem',problem_number=request.POST.get('LCNum'))
    else:
        return redirect('Data:index')
        

def problem(request, problem_number):
    if request.POST:
        return redirect('Data:postProblem')
    else:
        problem = Problem.objects.filter(problem_number=problem_number).first()
        if problem:
            context = {
                "problem" : problem,
                "solves" : problem.Solves.all().order_by("-date")[:15] 
            }
        else:
            context = {
                "problem_number" : problem_number
            }
        return render(request,"Data/problem.html",context=context)