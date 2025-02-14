from django.shortcuts import render


def Job(request):
    return render(request, 'jobs/jobs.html')
# Create your views here.
