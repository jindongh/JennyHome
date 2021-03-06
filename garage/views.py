from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from models import GarageOp
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone
import logging
import door
logger = logging.getLogger(__name__)

# Create your views here.
@login_required
@permission_required('garage.check')
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
@permission_required('garage.check')
def state(request):
    stateByDB = door.getDoorStateFromDB()
    stateByCV = door.getDoorStateFromCV()
    return JsonResponse({
        'stateFromDB': stateByDB,
        'stateFromCV': stateByCV
        })

@login_required
@permission_required('garage.operate')
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
            op_date = timezone.now(),
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
@permission_required('garage.check')
def doorImage(request):
    image = door.getDoorImage()
    return HttpResponse(image, content_type="image/jpeg")

@login_required
@permission_required('garage.check')
def cvImage(request):
    image = open(door.CV_IMAGE_PATH).read()
    return HttpResponse(image, content_type='image/jpeg')
