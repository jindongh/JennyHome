# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django_apscheduler.models import DjangoJob
from django_apscheduler.models import DjangoJobExecution
from garage import door

# Create your views here.
def home(request):
    jobs = DjangoJob.objects.all()
    return render(request, 'cronjobs/home.html', {'jobs': jobs})

def executions(request):
    jobId = request.GET['job'];
    execs = DjangoJobExecution.objects.filter(job__id=jobId)
    resp = [{
        'status': execution.status,
        'run_time': timezone.localtime(execution.run_time),
        } for execution in execs]
    return JsonResponse(resp, safe=False)

def run(request):
    doorState = door.getDoorStateFromCV()
    if doorState == door.DOOR_OPEN:
        return JsonResponse({'result':'Door is open'})
    else:
        return JsonResponse({'result':'Door is closed'})
