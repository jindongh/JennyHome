from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from models import GarageOp
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
import logging
import door
logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def home(request):
    history = GarageOp.objects.order_by('-op_date')[:10]
    curState = door.getDoorStateFromDB()
    newState = door.toggleDoorState(curState)
    context = {
            'history': history,
            'state': curState,
            'action': newState,
            }
    return render(request, 'garage/home.html', context)

@login_required
def state(request):
    stateByDB = door.getDoorStateFromDB()
    stateByCV = door.getDoorStateFromCV()
    return JsonResponse({
        'stateFromDB': stateByDB,
        'stateFromCV': stateByCV
        })

@login_required
def toggle(request):
    logger.info('Try to toggle garage door')
    succeed = False
    message = ''
    try:
        newState = door.toggleDoor()
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

@login_required
def doorImage(request):
    image = door.getDoorImage()
    return HttpResponse(image, content_type="image/jpeg")
