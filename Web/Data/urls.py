"""LeetcodeTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'Data'
urlpatterns = [
    path('',views.index,name="index"),
    path('solution/<id>',views.solution,name="solution"),
    path('member/<discord_id>',views.member,name="member"),
    path('problem_list',views.problemList,name="problemList"),
    path('problem',views.postProblem,name="postProblem"),
    path('problem/<problem_number>',views.problem,name="problem")
]
