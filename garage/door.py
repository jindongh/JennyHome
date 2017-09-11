from django.conf import settings
from models import GarageOp
import RPi.GPIO as GPIO
import cv2, numpy
import time

DOOR_OPEN = 'Open'
DOOR_CLOSE = 'Close'
DOOR_UNKNOWN = 'Unknown'
CV_IMAGE_PATH = '/tmp/%s/cv.jpg' % settings.DOMAIN
DOOR_PIN = 17

def toggleDoor():
    curState = getDoorStateFromDB()
    if GPIO.getmode() == None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, GPIO.HIGH)
    time.sleep(1) # Delay is necessary, otherwise it will not work.
    GPIO.output(17, GPIO.LOW)
    newState = toggleDoorState(curState)
    return newState

def getDoorStateFromDB():
    history = GarageOp.objects.order_by('-op_date')[:1]
    if len(history) == 0:
        return DOOR_CLOSE
    else:
        return history[0].op_type

def getDoorStateFromCV():
    image = getDoorImage()
    img_array = numpy.asarray(bytearray(image), dtype=numpy.uint8)
    img = cv2.imdecode(img_array, cv2.CV_LOAD_IMAGE_COLOR)
    height, width, channels = img.shape
    mask = numpy.zeros((height+2, width+2), numpy.uint8)
    start_pixel = (740, 310)
    diff = (3,3,3)
    retval, rect = cv2.floodFill(img, mask, start_pixel, (0,255,0), diff, diff)
    cv2.imwrite(CV_IMAGE_PATH, img)
    print retval
    if retval > 5000:
        return DOOR_CLOSE
    else:
        return DOOR_OPEN

def toggleDoorState(curState):
    if curState == DOOR_OPEN:
        return DOOR_CLOSE
    else:
        return DOOR_OPEN

def getDoorImage():
    blink = settings.BLINK
    network = blink.network('Home')
    camera = blink.camera(network, 'Garage')
    thumb = blink.capture_thumbnail(camera)
    image = blink.download_thumbnail(thumb)
    return image

