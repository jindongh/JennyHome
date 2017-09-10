from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from models import GarageOp
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
from django.conf import settings
import cv2
import numpy
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
    stateByDB = _getDoorStateFromDB()
    stateByCV = _getDoorStateFromCV()

    return JsonResponse({
        'stateFromDB': stateByDB,
        'stateFromCV': stateByCV
        })

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
    curState = _getDoorStateFromDB()
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

@login_required
def doorImage(request):
    image = _getDoorImage()
    return HttpResponse(image, content_type="image/jpeg")

def _getDoorStateFromCV():
    image = _getDoorImage()
    img_array = numpy.asarray(bytearray(image), dtype=numpy.uint8)
    img = cv2.imdecode(img_array, cv2.CV_LOAD_IMAGE_COLOR)
    height, width, channels = img.shape
    mask = numpy.zeros((height+2, width+2), numpy.uint8)
    start_pixel = (640, 310)
    diff = (3,3,3)
    retval, rect = cv2.floodFill(img, mask, start_pixel, (0,255,0), diff, diff)
    if retval > 10000:
        return DOOR_CLOSE
    else:
        return DOOR_OPEN

def _getDoorImage():
    blink = settings.BLINK
    network = blink.network('Home')
    camera = blink.camera(network, 'Garage')
    thumb = blink.capture_thumbnail(camera)
    image = blink.download_thumbnail(thumb)
    return image

def _getDoorStateFromDB():
    history = GarageOp.objects.order_by('-op_date')[:1]
    return _getDoorStateFrom(history)
