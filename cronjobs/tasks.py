from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.jobstores import register_events
from django.conf import settings
from garage import door
import boto3

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')
scheduler.add_executor(ThreadPoolExecutor(10))
sns=boto3.client('sns')

@scheduler.scheduled_job('interval',
        id='VerifyGarageDoorIsClose',
        days=1,
        start_date='2017-09-01 22:00:30')
def doorIsOpen():
    state = door.getDoorStateFromCV()
    if state == door.DOOR_CLOSE:
        return 'Door is closed'
    url = 'http://%s/garage/api/cv' % (settings.DOMAIN)
    for phone in settings.ADMIN_PHONES:
        sns.publish(
                PhoneNumber=settings.phone,
                Message='Garage door is OPEN %s' % url)

def is_door_close():
    print 'Door is closed'

register_events(scheduler)
scheduler.start()

