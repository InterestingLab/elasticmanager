from __future__ import absolute_import

from datetime import timedelta
from functools import wraps

from celery import shared_task
from django.db.models import Q
from cluster.models import ElasticCluster # flake8: noqa
from .exceptions import CanNotCloseIndex, CanNotCreateIndex, CanNotDeleteIndex
from .indexset import IndexSetObj
from .models import IndexSet, TaskExec
from .utils import timenow


# threshold of healthy elasticsearch cluster in yellow status
MAX_INITIALIZING_SHARDS = 50
MAX_UNASSIGNED_SHARDS = 10
MAX_NUMBER_OF_PENDING_TASKS = 500


def healthy_cluster(**decorator_kwargs):
    """healthy cluster decorator with arguments
       decorator_kwargs can be:
           initializing_shards
           unassigned_shards
           number_of_pending_tasks
    """

    default = {
        'initializing_shards': MAX_INITIALIZING_SHARDS,
        'unassigned_shards': MAX_UNASSIGNED_SHARDS,
        'number_of_pending_tasks': MAX_NUMBER_OF_PENDING_TASKS,
    }
    decorator_kwargs.update(default)

    def real_decorator(func):

        # functools.wraps() decorator copies all the necessary metadata over from func to the wrapper
        @wraps(func)
        def wrapped_func(clusteri_id, *args, **kwargs):

            es = ElasticCluster.objects.get(pk=clusteri_id)

            status =es.health()
            if status['status'].lower() == 'red' \
                or (status['status'].lower() == 'yellow' \
                    and (status['initializing_shards'] > decorator_kwargs['initializing_shards'] \
                        or status['unassigned_shards'] > decorator_kwargs['unassigned_shards'] \
                        or status['number_of_pending_tasks'] > decorator_kwargs['number_of_pending_tasks'])):

                return 0

            return func(clusteri_id, *args, **kwargs)

        return wrapped_func

    return real_decorator


# batch number of creating indexset
CREATE_BATCH = 5
# batch number of closing indexset
CLOSE_BATCH = 5
# batch number of deleting indexset
DELETE_BATCH = 5


@shared_task
@healthy_cluster()
def create_indices(clusteri_id):
    """return number of indices created
    """
    yesterday = timenow() - timedelta(days=1)

    # filter(indexset__elasticsearch__pk=clusteri_id) join by Indexset and ElasticCluster
    task_execs = TaskExec.objects \
                 .filter(indexset__elasticsearch__pk=clusteri_id) \
                 .filter(type=TaskExec.TaskType.CREATE) \
                 .filter(Q(last_run_status=TaskExec.Status.FAILURE) | Q(last_run_at__lte=yesterday)) \
                 .order_by('last_run_at')[:CREATE_BATCH]

    indices_created = 0
    for t in task_execs:
        iset = IndexSetObj(t.indexset)

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
@healthy_cluster()
def close_indices(clusteri_id):
    """return number of indices closed
    """
    yesterday = timenow() - timedelta(days=1)

    # filter(indexset__elasticsearch__pk=clusteri_id) join by Indexset and ElasticCluster
    task_execs = TaskExec.objects \
                 .filter(indexset__elasticsearch__pk=clusteri_id) \
                 .filter(type=TaskExec.TaskType.CLOSE) \
                 .filter(Q(last_run_status=TaskExec.Status.FAILURE) | Q(last_run_at__lte=yesterday)) \
                 .order_by('last_run_at')[:CLOSE_BATCH]

    indices_closed = 0
    for t in task_execs:
        iset = IndexSetObj(t.indexset)

        try:
            indices_closed += iset.close()
            t.last_run_status = TaskExec.Status.SUCCESS

        except CanNotCloseIndex as e:
            t.last_run_status = TaskExec.Status.FAILURE
            t.last_run_info = str(e)

        t.last_run_at = timenow()
        t.save()

    return indices_closed


@shared_task
@healthy_cluster()
def delete_indices():
    """return number of indices deleted
    """
    yesterday = timenow() - timedelta(days=1)

    # filter(indexset__elasticsearch__pk=clusteri_id) join by Indexset and ElasticCluster
    task_execs = TaskExec.objects \
                 .filter(indexset__elasticsearch__pk=clusteri_id) \
                 .filter(type=TaskExec.TaskType.DELETE) \
                 .filter(Q(last_run_status=TaskExec.Status.FAILURE) | Q(last_run_at__lte=yesterday)) \
                 .order_by('last_run_at')[:DELETE_BATCH]

    indices_deleted = 0
    for t in task_execs:
        iset = IndexSetObj(t.indexset)

        try:
            indices_deleted += iset.delete()
            t.last_run_status = TaskExec.Status.SUCCESS

        except CanNotDeleteIndex as e:
            t.last_run_status = TaskExec.Status.FAILURE
            t.last_run_info = str(e)

        t.last_run_at = timenow()
        t.save()

    return indices_deleted
