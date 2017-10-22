# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
import uuid,requests

from .models import Script

# Create your views here.
def home(request):
    return render(request, 'puppeteer/home.html')

def execute(request):
    URL='http://127.0.0.1:8080'
    data = {'id': str(uuid.uuid4()),
            'script': request.POST['script']}
    try:
        response = requests.post(URL, data=data)
        return JsonResponse(response.json())
    except Exception, e:
        return JsonResponse({
            'code': -1,
            'stdout': '',
            'stderr': str(e)
            })

def list_all(request):
    scripts = Script.objects.filter(user = request.user.is_active and request.user or None)
    return JsonResponse([_script2Json(script, includeCode=False)
        for script in scripts], safe = False)

def get(request, codeId):
    script = Script.objects.get(pk=codeId)
    return JsonResponse(_script2Json(script))

def update(request):
    if 'id' in request.POST and request.POST['id'] != '':
        script = Script.objects.get(pk=request.POST['id'])
    else:
        script = Script(user = request.user.is_active and request.user or None)
    script.name = request.POST['name']
    script.code = request.POST['code']
    script.save()
    return JsonResponse(_script2Json(script, includeCode=False))

def delete(request, codeId):
    script = Script.objects.get(pk=codeId)
    resp = _script2Json(script, includeCode=False)
    script.delete()
    return JsonResponse(resp)

def _script2Json(script, includeCode=True):
    resp = {
            'id': script.id,
            'name': script.name,
            'created': script.created,
            'updated': script.updated,
            }
    if includeCode:
        resp['code'] = script.code
    return resp
