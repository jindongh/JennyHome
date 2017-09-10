# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django_apscheduler.models import DjangoJob
from django_apscheduler.models import DjangoJobExecution

# Create your views here.
def home(request):
    jobs = DjangoJob.objects.all()
    return render(request, 'cronjobs/home.html', {'jobs': jobs})

def executions(request):
    jobId = request.GET['job'];
    execs = DjangoJobExecution.objects.filter(job__id=jobId)
    resp = [{
        'status': execution.status,
        'run_time': execution.run_time,
        } for execution in execs]
    return JsonResponse(resp, safe=False)

def run(request):
    pass
