from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class ElasticCluster(models.Model):
    class Meta:
        db_table = 'cluster_elastic_cluster'

    # cluster name
    name = models.CharField(max_length=128)
    host = models.CharField(max_length=256)
    port = models.IntegerField()

    def __str__(self):
        return '{name} {host}:{port}'.format(name=self.name, host=self.host, port=self.port)

    def address(self):
        return '{host}:{port}'.format(host=self.host, port=self.port)
