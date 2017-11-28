# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from django.utils import timezone
from django.http import Http404, JsonResponse, HttpResponseForbidden

from django.shortcuts import render
from .models import Thing, Operation
from garage import door

THING_DISPLAY = "Display"
THING_RELAY = 'Relay'
THING_TEMPERATURE = 'Temperature'
THING_DOOR = 'Door'

PLACE_THERMOSTAT = 'thermostat'
PLACE_BACKLIGHT = 'backlight'

# decorator
def lan_restricted(view_func):
    def func_wrapper(request, *args, **kwargs):
        client_address = request.META['HTTP_X_FORWARDED_FOR'] 
        if client_address.startswith('192.168.86.'):
            return view_func(request, *args, **kwargs)
        else:
            raise HttpResponseForbidden()
    return func_wrapper

def home(request):
    things = Thing.objects.order_by('-updated')
    return render(request, 'iot/home.html', {'things': things})

@lan_restricted
def relay(request):
    thingType = THING_RELAY
    return getOrSet(request, thingType)

@lan_restricted
def display(request):
    thingType = THING_DISPLAY
    return getOrSet(request, thingType)
ALIAS = {
        ('line1', THING_DISPLAY):('bedroom', THING_TEMPERATURE),
        ('line2', THING_DISPLAY):('thermostat', THING_RELAY),
        }
def getOrSet(request, thingType):
    if not 'place' in request.GET:
        raise Http404
    place = request.GET['place']
    if not 'value' in request.GET:
        if (place, thingType) in ALIAS:
            place, thingType = ALIAS[(place, thingType)]
        try:
            thing = Thing.objects.get(pk=_getId(place, thingType))
            return JsonResponse({
                "updated":thing.updated.strftime('%s'),
                "state":thing.state})
        except:
            raise Http404
    else:
        return updateThing(thingType, request.GET['place'], request.GET['value'])

@lan_restricted
def temperature(request):
    if (not 'place' in request.GET) or (not 'value' in request.GET):
        raise Http404
    return updateThing(THING_TEMPERATURE, request.GET['place'], request.GET['value'])


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
        '68:37:e9:68:76:9e':'Thermostat', #Basics
        '18:74:2e:93:10:2f': 'Display', # display
        '78:e1:03:5e:0e:39': 'Door', # Fiji
        }
IGNORE_MACS = [
        '2c:3a:e8:2f:80:24', # .21 Thermostat
        '2c:3a:e8:2f:83:85', # .22 Temperature
        '2c:3a:e8:2f:80:ad', # .23 LCD
        'b8:27:eb:41:b1:43', # .100 Pi
        # 
        '50:c7:bf:2b:d4:e6', # Light
        '50:f5:da:f0:1a:c4', # Echo
        '00:03:7f:b9:13:e5', # Wander
        'j', # Blink
        '00:bb:c1:25:24:30', # Printer
        'd8:e0:e1:82:9c:aa', # TV
        # Laptop
        '8c:85:90:56:4d:3d', #Azuqua
        '', #Jenny-Mac
        '2c:f0:ee:08:6f:82', #Hank-Mac
        # Phone
        '28:a0:2b:ab:9f:3e', #Jenny-iPhone
        '94:65:2d:6e:2b:56', #Hank-OnePlus
        '10:f1:f2:00:9c:24', #LG
        ]
def dashButtonEvent(mac):
    if mac in DASH_BUTTON_DICT:
        place = DASH_BUTTON_DICT[mac]
    else:
        if not mac in IGNORE_MACS:
            print 'Unknown mac %s' % mac
        return
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
        updateThing(THING_RELAY, PLACE_THERMOSTAT, thing.state)
    elif place == 'Door':
        door.toggleDoor()
    elif place == 'Display':
        updateThing(THING_DISPLAY, PLACE_BACKLIGHT, thing.state)


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
    return '%s_%s' % (thingType, re.sub(':', '_', place))

def _saveHistory(thing, event):
    operation = Operation(thing=thing, event=event)
    operation.save()

