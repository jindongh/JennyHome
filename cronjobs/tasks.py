from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.jobstores import register_events

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')
scheduler.add_executor(ThreadPoolExecutor(10))

@scheduler.scheduled_job('interval',
        id='VerifyGarageDoorIsClose',
        days=1,
        start_date='2017-09-01 22:00:30')

def doorIsOpen():
    print('Door is Open/Close')

def is_door_close():
    print 'Door is closed'

register_events(scheduler)
scheduler.start()

