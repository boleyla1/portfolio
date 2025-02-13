import jdatetime
from django.shortcuts import render
from .models import Skill, Project, RecentProject, Service


def index(request):
    Projects = Project.objects.all()
    Skills = Skill.objects.all()
    RecentProjects = RecentProject.objects.all()
    Services = Service.objects.all()
    created_at_shamsi = Project.end_date_shamsi
    return render(request, 'mainapp/index.html', {"projects": Projects, 'skills': Skills,
                                                  'recent_projects': RecentProjects, 'services': Services,
                                                  'created_at_shamsi': created_at_shamsi})


def about(request):
    return render(request, 'about/about.html')



