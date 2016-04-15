from __future__ import unicode_literals
from django.db import models
from django_enumfield import enum

class IndexSet(models.Model):

    class EnumEsIndexTimeInterval(enum.Enum):
        HOURS = 0
        DAYS = 1
        WEEKS = 2
        MONTHS = 3
        YEARS = 4

    class EnumStatus(enum.Enum):
        STARTED = 0
        STOPPED = 1

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    index_name_prefix = models.CharField(max_length=256)
    # Note: available timestring defined in:
    #       https://docs.python.org/2.7/library/datetime.html#strftime-strptime-behavior
    index_timestring = models.CharField(max_length=32)
    index_timestring_interval = enum.EnumField(EnumEsIndexTimeInterval, default=EnumEsIndexTimeInterval.DAYS)
    elasticsearch = models.CharField(max_length=32)
    created_at = models.DateTimeField()
    status = enum.EnumField(EnumStatus, default=EnumStatus.STARTED)

    class Meta:
        db_table = 'index_set'


class CreateIndexAction(models.Model):
    class Meta:
        db_table = 'create_index_action'

    index_set = models.ForeignKey(IndexSet, on_delete=models.CASCADE)


class OptimizeIndexAction(models.Model):
    class Meta:
        db_table = 'optimize_index_action'

    index_set = models.ForeignKey(IndexSet, on_delete=models.CASCADE)
    optimize_after_days = models.IntegerField()


class CloseAction(models.Model):
    class Meta:
        db_table = 'close_index_action'

    index_set = models.ForeignKey(IndexSet, on_delete=models.CASCADE)
    close_after_days = models.IntegerField()


class DeleteAction(models.Model):
    class Meta:
        db_table = 'delete_index_action'

    index_set = models.ForeignKey(IndexSet, on_delete=models.CASCADE)
    delete_after_days = models.IntegerField()


class SnapshotAction(models.Model):
    class Meta:
        db_table = 'snapshot_index_action'

    index_set = models.ForeignKey(IndexSet, on_delete=models.CASCADE)


class IndexMappings(models.Model):
    class Meta:
        db_table = 'index_mappings'


class IndexSettings(models.Model):
    class Meta:
        db_table = 'index_settings'
