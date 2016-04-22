from __future__ import unicode_literals
from django.db import models
from django_enumfield import enum
from cluster.models import ElasticCluster
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
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

    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256, blank=True)
    index_name_prefix = models.CharField(max_length=256)
    # Note: available timestring defined in:
    #       https://docs.python.org/2.7/library/datetime.html#strftime-strptime-behavior
    index_timestring = models.CharField(max_length=32)
    index_timestring_interval = enum.EnumField(EnumEsIndexTimeInterval, default=EnumEsIndexTimeInterval.DAYS)
    elasticsearch = models.ForeignKey(ElasticCluster, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timenow)
    status = enum.EnumField(EnumStatus, default=EnumStatus.STARTED)

    class Meta:
        db_table = 'indices_index_set'

    def __str__(self):
        return self.name


class TaskExec(models.Model):
    class Meta:
        db_table = 'indices_tasks'

    class TaskType(enum.Enum):
        ALIAS = 0
        CLOSE = 1
        CREATE = 2
        DELETE = 3
        OPTIMIZE = 4
        SNAPSHOT = 5

    class Status(enum.Enum):
        SUCCESS = 0
        FAILURE = 1

    index_set = models.ForeignKey(IndexSet, on_delete=models.CASCADE)
    type = enum.EnumField(TaskType)
    last_run_at = models.DateTimeField(default=timenow)
    last_run_status = enum.EnumField(Status, default=Status.SUCCESS)
    last_run_info = models.TextField(default='')


@python_2_unicode_compatible
class Create(models.Model):
    class Meta:
        db_table = 'indices_create'

    index_set = models.OneToOneField(IndexSet, on_delete=models.CASCADE)
    exec_offset = models.IntegerField()
    # follow the mappings of last existing index
    follow_mappings = models.BooleanField()

    def __str__():
        return self.index_set


@python_2_unicode_compatible
class Optimize(models.Model):
    class Meta:
        db_table = 'indices_optimize'

    index_set = models.OneToOneField(IndexSet, on_delete=models.CASCADE)
    exec_offset = models.IntegerField()
    target_segment_num = models.IntegerField()

    def __str__():
        return self.index_set


@python_2_unicode_compatible
class Close(models.Model):
    class Meta:
        db_table = 'indices_close'

    index_set = models.OneToOneField(IndexSet, on_delete=models.CASCADE)
    exec_offset = models.IntegerField()

    def __str__():
        return self.index_set


@python_2_unicode_compatible
class Delete(models.Model):
    class Meta:
        db_table = 'indices_delete'

    index_set = models.OneToOneField(IndexSet, on_delete=models.CASCADE)
    exec_offset = models.IntegerField()

    def __str__():
        return self.index_set


@python_2_unicode_compatible
class Snapshot(models.Model):
    class Meta:
        db_table = 'indices_snapshot'

    index_set = models.OneToOneField(IndexSet, on_delete=models.CASCADE)
    exec_offset = models.IntegerField()

    def __str__():
        return self.index_set


@python_2_unicode_compatible
class Alias(models.Model):
    class Meta:
        db_table = 'indices_alias'

    index_set = models.OneToOneField(IndexSet, on_delete=models.CASCADE)

    def __str__():
        return self.index_set


@python_2_unicode_compatible
class Mappings(models.Model):
    class Meta:
        db_table = 'indices_mappings'

    index_set = models.OneToOneField(IndexSet, on_delete=models.CASCADE)
    mappings = models.TextField()

    def __str__():
        return ''


@python_2_unicode_compatible
class Settings(models.Model):
    class Meta:
        db_table = 'indices_settings'

    index_set = models.OneToOneField(IndexSet, on_delete=models.CASCADE)
    settings = models.TextField()

    def __str__():
        return ''
