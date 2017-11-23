# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import render
from .models import Thing, Operation

# decorator
def lan_restricted(view_func):
    def func_wrapper(request, *args, **kwargs):
        client_address = request.META['HTTP_X_FORWARDED_FOR'] 
        if client_address.startswith('192.168.86.'):
            return view_func(request, *args, **kwargs)
        else:
            raise Http404
    return func_wrapper

def home(request):
    things = Thing.objects.all()
    return render(request, 'iot/home.html', {'things': things})

@lan_restricted
def relay(request):
    thingType = 'Relay'
    if not 'place' in request.GET:
        raise Http404
    place = request.GET['place']
    if not 'value' in request.GET:
        try:
            thing = Thing.objects.get(pk=_getId(place, thingType))
            if thing.state == 'on':
                return JsonResponse({
                    'isOn': True
                    })
        except:
            pass
        raise Http404
    else:
        return updateThing(thingType, request.GET['place'], request.GET['value'])

@lan_restricted
def temperature(request):
    #if (not 'place' in request.GET) or (not 'vlaue' in request.GET):
    #    raise Http404
    return updateThing('Temperature', request.GET['place'], request.GET['value'])

@lan_restricted
def setName(request):
    '''
    id = request.GET['id']
    name = request.GET['name']
    thing = Thing.objects.get(pk=id)
    thing.name = name
    thing.save()
    '''
    return JsonResponse({
        'attr':request.hjz,
        'succeed': True
        })
DASH_BUTTON_DICT = {
        '68:37:e9:68:76:9e':'Thermostat'
        }
def dashButtonEvent(mac):
    if mac in DASH_BUTTON_DICT:
        place = DASH_BUTTON_DICT[mac]
    else:
        place = mac
    thingType = 'DashButton'
    id = _getId(place, thingType)
    try:
        thing = Thing.objects.get(pk=id)
    except:
        thing = Thing(id=id, name=id, state='off')
    thing.state = thing.state == 'on' and 'off' or 'on'
    thing.save()
    _saveHistory(thing, thingType + ' is ' + thing.state)
    if place == 'Thermostat':
        updateThing('Relay', 'thermostat', thing.state)

def updateThing(thingType, place, value):
    id = _getId(place, thingType)
    try:
        thing = Thing.objects.get(pk=id)
        thing.state = value
    except:
        thing = Thing(id = id, name = id, state = value)
    thing.save()
    _saveHistory(thing, thingType + ' is ' + value)
    return JsonResponse({
        'succeed': True
        })

def history(request):
    thingId = request.GET['thing']
    operations = Operation.objects.filter(thing__id=thingId).order_by('-created')[:10]
    return JsonResponse([
        {
            'time':timezone.localtime(operation.created),
            'event':operation.event
            } for operation in operations
        ], safe=False)

def _getId(place, thingType):
    return '%s_%s' % (thingType, place)

def _saveHistory(thing, event):
    operation = Operation(thing=thing, event=event)
    operation.save()

