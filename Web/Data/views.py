from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .models import *

# Create your views here.
def index(request):
    solves = Solve.objects.all().order_by("-date")
    paginator = Paginator(solves,10)
    context = {
        "solves_page" : paginator.get_page(request.GET.get('page')),
        "pagination" : paginator.num_pages != 1
    }
    return render(request, "Data/index.html", context=context)

def solution(request,id):
    solves = Solve.objects.filter(pk=id).first()
    if solves:
        problemSolves = solves.problem.Solves.all().order_by("-date")
        paginator = Paginator(problemSolves,10)
        context = {
            "solve" : solves,
            "problem_solves":paginator.get_page(request.GET.get('page')),
            "pagination" : paginator.num_pages != 1
        }
    else:
        context = {
            "id" : id
        }
    return render(request, "Data/solution.html",context=context)

def member(request, discord_id):
    user = Member.objects.filter(discordID=discord_id).first()
    if user:
        userSolves = user.Solves.all().order_by("-date")
        paginator = Paginator(userSolves,10)
        context = {
            "member" : user,
            "userSolves" : paginator.get_page(request.GET.get('page')),
            "pagination" : paginator.num_pages != 1
        }
    else:
        context = {
            "discordID" : discord_id
        }
    return render(request, "Data/member.html", context=context)

def problemList(request):
    problems = Problem.objects.all().order_by("problem_number")
    paginator = Paginator(problems,10)
    context = {
        "Problems" : paginator.get_page(request.GET.get('page')),
        "pagination" : paginator.num_pages != 1
    }
    return render(request,"Data/problem_list.html",context=context)

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
            problemSolves = problem.Solves.all().order_by("-date")
            paginator = Paginator(problemSolves,10)
            context = {
                "problem" : problem,
                "problem_solves" : paginator.get_page(request.GET.get('page')),
                "pagination" : paginator.num_pages != 1
            }
        else:
            context = {
                "problem_number" : problem_number
            }
        return render(request,"Data/problem.html",context=context)