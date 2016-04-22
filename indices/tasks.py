from __future__ import absolute_import
from datetime import datetime, timedelta
from celery import shared_task
from django.db.models import Q
from .indexset import IndexSetObj
from .models import IndexSet


# batch number of creating indices
CREATE_BATCH = 5

@shared_task
def create_indices():
    from django.utils import timezone
    from .models import TaskExec

    # TODO: check cluster health first and divide create_indices task(arg:cluster) by elasticsearch cluster

    yesterday = timezone.now() - timedelta(days=1)
    task_execs = TaskExec.objects \
                 .filter(type=TaskExec.TaskType.CREATE) \
                 .filter(Q(last_run_status=TaskExec.Status.FAILURE) | Q(last_run_at__lte=yesterday)) \
                 .order_by('last_run_at')[:CREATE_BATCH]

    indices_created = 0
    for t in task_execs:
        iset = IndexSetObj(ex.index_set)

        try:
            indices_created += iset.create()
            t.last_run_status = TaskExec.Status.SUCCESS

        except CanNotCreateIndex as e:
            t.last_run_status = TaskExec.Status.FAILURE
            t.last_run_info = str(e)

        t.last_run_at = timenow()
        t.save()

    return indices_created


@shared_task
def optimize_indices():
    pass


@shared_task
def close_indices():
    pass


@shared_task
def delete_indices():
    pass

