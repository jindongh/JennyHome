from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from models import GarageOp
from django.http import JsonResponse
from datetime import datetime

import logging
logger = logging.getLogger(__name__)
DOOR_OPEN = 'Open'
DOOR_CLOSE = 'Close'
DOOR_UNKNOWN = 'Unknown'

# Create your views here.
@login_required
def home(request):
    history = GarageOp.objects.order_by('-op_date')[:10]
    curState = _getDoorStateFrom(history)
    newState = _getNextDoorState(curState)
    context = {
            'history': history,
            'state': curState,
            'action': newState,
            }
    return render(request, 'garage/home.html', context)

@login_required
def state(request):
    curState = _getDoorState()
    return JsonResponse({'state': curState})

@login_required
def toggle(request):
    logger.info('Try to toggle garage door')
    newState = DOOR_UNKNOWN
    succeed = False
    message = ''
    try:
        newState = _toggleDoorState()
        succeed = True
        logger.info('Garage door is ' + newState)
    except Exception, e:
        logger.error('Failed to toggle Door: ' + e)
        message = str(e)
    op = GarageOp(
            op_type = newState,
            op_date = datetime.now(),
            op_succeed = succeed,
            error_message = message
            )
    op.save()
    return JsonResponse({
        'type': op.op_type,
        'date': op.op_date,
        'succeed': op.op_succeed,
        'error': op.error_message
        })

def _toggleDoorState():
    curState = _getDoorState()
    newState = _getNextDoorState(curState)
    # Change door with RPi.GPIO
    return newState

def _getNextDoorState(curState):
    if curState == DOOR_OPEN:
        return DOOR_CLOSE
    else:
        return DOOR_OPEN

def _getDoorStateFrom(history):
    if len(history) == 0:
        return DOOR_CLOSE
    else:
        return history[0].op_type

def _getDoorState():
    history = GarageOp.objects.order_by('-op_date')[:1]
    return _getDoorStateFrom(history)
