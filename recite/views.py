# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from datetime import datetime,timedelta
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from cronjobs.tasks import scheduler
from cronjobs.tasks import sns
from .models import Setting,Item

# Create your views here.
@login_required
def home(request):
    setting = _getOrCreateSetting(request.user)
    return render(request, 'recite/home.html', {'key': setting.key})

@csrf_exempt
def getKey(request):
    user = authenticate(request.POST['username'], password=request.POST['password'])
    if user is None:
        return HttpResponseNotAllowed()
    setting = _getOrCreateSetting(user)

    return setting.key

@csrf_exempt
def history(request):
    setting = _getSetting(request)
    items = Item.objects.filter(user=setting.user)
    return JsonResponse([_item2Json(item) for item in items], safe=False)

@csrf_exempt
def setting(request):
    setting = _getSetting(request)
    if request.method=='GET':
        return JsonResponse(_setting2Json(setting), safe=False)
    else:
        setting.sms = request.POST['sms']
        setting.email = request.POST['email']
        setting.mobile = request.POST['mobile']
        setting.notAfter = int(request.POST['notAfter'])
        setting.notBefore = int(request.POST['notBefore'])
        setting.save()
        return JsonResponse(_setting2Json(setting), safe=False)

@csrf_exempt
def add(request):
    setting = _getSetting(request)
    item = Item(user = setting.user,
            content = request.POST['content'])
    item.save()
    _scheduleJob(item, setting)
    return JsonResponse(_item2Json(item))

@csrf_exempt
def delete(request):
    item = Item.objects.get(pk=request.GET['id'])
    try:
        scheduler.remove_job(_getJobId(item))
    except:
        pass
    item.delete()
    return JsonResponse({})

def _notifyJob(item, setting):
    if setting.sms != '':
        phone = setting.sms.startswith('+1') and setting.sms or '+1'+setting.sms
        sns.publish(
                PhoneNumber=phone,
                Message=item.content)
    if setting.email != '':
        print('send %s to email %s' % (item.content, setting.email))
    if setting.mobile != '':
        print('send %s to mobile %s' % (item.content, setting.mobile))
    print('Notify Over')
    _scheduleJob(item, setting)

def _getJobId(item):
    return 'Recite-%d' % item.id

def _scheduleJob(item, setting):
    diff = (timezone.now() - item.created).total_seconds()
    steps = [3600, 3600*24, 3600*24*7]
    for step in steps:
        if diff < step:
            print("Found right diff %d" % diff)
            run_date = item.created + timedelta(seconds=step)
            scheduler.add_job(_notifyJob, 'date',
                    run_date=run_date,
                    args=(item, setting),
                    replace_existing = True,
                    id=_getJobId(item))
            return 'Scheduled at %s' % run_date
    return 'Removed'

def _item2Json(item):
    return {
            'id': item.id,
            'content': item.content,
            'created': timezone.localtime(item.created)
            }
def _setting2Json(setting):
    return {
            'id': setting.id,
            'sms': setting.sms,
            'email': setting.email,
            'mobile': setting.mobile,
            'notAfter': setting.notAfter,
            'notBefore': setting.notBefore
            }


def _getSetting(request):
    key = request.method == 'GET' and request.GET['key'] or request.POST['key']
    setting = Setting.objects.filter(key=key).first()
    if setting is None:
        raise PerissionDenied()
    else:
        return setting

def _getOrCreateSetting(user):
    setting = Setting.objects.filter(user=user).first()
    if setting is not None:
        return setting
    else:
        setting = Setting(
                user = user,
                key = uuid.uuid4())
        setting.save()
        return setting
