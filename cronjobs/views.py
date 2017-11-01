# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django_apscheduler.models import DjangoJob
from django_apscheduler.models import DjangoJobExecution
from garage import door
from .tasks import scheduler
from .models import Workflow
from .executor import Executor

# Create your views here.
def home(request):
    jobs = DjangoJob.objects.all()
    return render(request, 'cronjobs/home.html', {'jobs': jobs})

def executions(request):
    jobId = request.GET['job'];
    execs = DjangoJobExecution.objects.filter(job__id=jobId)[:10]
    resp = [{
        'status': execution.status,
        'run_time': timezone.localtime(execution.run_time),
        'exception': execution.exception,
        'traceback': execution.traceback,
        'retval': execution.retval,
        } for execution in execs]
    return JsonResponse(resp, safe=False)

def list_workflow(request):
    workflows = Workflow.objects.filter(user=request.user)
    return JsonResponse([{
        'id': workflow.id,
        'name': workflow.name
        } for workflow in workflows], safe=False)

def get_workflow(request, id):
    workflow = Workflow.objects.get(pk=id)
    return JsonResponse(_workflow2Json(workflow, includeData=True))

def run_workflow(request):
    task = Executor(request.POST['id'])
    params = request.POST['params']
    result = task.execute(params)
    return JsonResponse(result)

def update_workflow(request):
    workflowId = request.POST['id']
    name = request.POST['name']
    data = request.POST['data']
    if workflowId == '':
        workflow = Workflow(user=request.user)
    else:
        workflow = Workflow.objects.get(pk=workflowId)
    workflow.name = name
    workflow.data = data
    workflow.save()
    return JsonResponse({
        'id': workflow.id,
        'name': workflow.name
        })

def delete_workflow(request, id):
    workflow = Workflow.objects.get(pk=id)
    response = _workflow2Json(workflow)
    workflow.delete();
    return JsonResponse(response)

def pause_workflow(request, jobId):
    scheduler.pause_job(jobId)
    return JsonResponse({})

def resume_workflow(request, jobId):
    scheduler.resume_job(jobId)
    return JsonResponse({})

def list_step(request):
    pass

def update_step(request):
    pass

def delete_step(request, stepId):
    pass

def test(request):
    doorState = door.getDoorStateFromCV()
    if doorState == door.DOOR_OPEN:
        return JsonResponse({'result':'Door is open'})
    else:
        return JsonResponse({'result':'Door is closed'})

def _workflow2Json(workflow, includeData = False):
    response = {
            'id': workflow.id,
            'name': workflow.name
            }
    if includeData:
        response['data'] = workflow.data
    return response
