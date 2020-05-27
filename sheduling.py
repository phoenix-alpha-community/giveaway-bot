import asyncio
import config
import transaction
from datetime import datetime

_scheduler = None

def delayed_execute(func, args, timedelta):
    exec_time = datetime.now(config.TIMEZONE) + timedelta

    id = _scheduler.add_job(_execute_wrapper, 'date',
            args=[func]+args, run_date = exec_time).id
    return id

async def _execute_wrapper(func, *args, **kwargs):
    ret = func(*args, **kwargs)
    if asyncio.iscoroutine(ret):
        ret = await ret
    transaction.commit()
    return ret