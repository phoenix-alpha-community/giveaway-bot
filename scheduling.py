import asyncio
import config
import sys
import transaction
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime


channel_ids_grace_period = set()

jobstores = {
    'default': SQLAlchemyJobStore(
        url='sqlite:///' + config.SCHEDULER_DB_FILENAME)
}

_scheduler = None


def init_scheduler():
    sys.stdout.write("Starting scheduler...")
    global _scheduler
    _scheduler = AsyncIOScheduler(jobstores=jobstores,
                                  job_defaults={
                                      'misfire_grace_time': None
                                  }
                                  )
    _scheduler.start()
    sys.stdout.write("done\n")


def delayed_execute(func, args, exec_time: datetime):

    id = _scheduler.add_job(_execute_wrapper, 'date',
                            args=[func] + args, run_date=exec_time).id
    return id


# wrap function to include transaction.commit
async def _execute_wrapper(func, *args, **kwargs):
    ret = func(*args, **kwargs)
    if asyncio.iscoroutine(ret):
        ret = await ret
    transaction.commit()
    return ret


def deschedule(job_id):
    _scheduler.remove_job(job_id)
