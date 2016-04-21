from __future__ import absolute_import
from datetime import datetime, timedelta
from celery import shared_task
from django.db.models import Q
from .indexset import IndexSetObj
from .models import IndexSet


@shared_task
def create_indices():
    from .models import Create, ActionStatus
    yesterday = datetime.now() - timedelta(days=1)
    objs = Create.objects.filter(Q(last_run_status=ActionStatus.FAILURE) | Q(__lte=yesterday))


@shared_task
def optimize_indices():
    pass


@shared_task
def close_indices():
    pass


@shared_task
def delete_indices():
    pass

