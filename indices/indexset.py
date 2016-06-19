import json

import curator
import elasticsearch

from .exceptions import CanNotCloseIndex, CanNotCreateIndex, CanNotDeleteIndex, CanNotRelocateIndex, CanNotReplicateIndex
from .utils import indices_in_days, reset_allocation, select_indices


class IndexSetObj(object):
    def __init__(self, model):
        self.model = model
        self.es = self.model.elasticsearch.client(timeout=120)

    def alias(self):
        pass

    def close(self):
        """return number of indices closed
        """
        indices = select_indices(
            self.es,
            self.model.index_name_prefix,
            self.model.index_timestring,
            self.model.index_timestring_interval,
            self.model.close.exec_offset
        )

        indices_closed = len(indices)

        if indices_closed > 0:
            try:
                ret = curator.close_indices(self.es, indices)
            except elasticsearch.exceptions.ConnectionTimeout as e:
                raise CanNotCloseIndex(str(e))

        return indices_closed

    def create(self):
        """return number of indices created
        """

        indices = indices_in_days(
            self.model.create.exec_offset,
            self.model.index_name_prefix,
            self.model.index_timestring,
            self.model.index_timestring_interval
        )

        settings = json.loads(self.model.settings.settings)
        mappings = json.loads(self.model.mappings.mappings)
        conf = {
            'settings': settings,
            'mappings': mappings,
        }

        indices_created = 0
        for index in indices:
            if not self.es.indices.exists(index):
                try:
                    # ignore 400 cause by IndexAlreadyExistsException when creating an index
                    ret = self.es.indices.create(index=index, body=conf, ignore=400)
                except elasticsearch.exceptions.ConnectionTimeout as e:
                    raise CanNotCreateIndex(str(e))

                if 'acknowledged' in ret and ret['acknowledged'] is True:
                    # {u'acknowledged': True}
                    indices_created += 1

                elif 'status' in ret and ret['status'] != 400:
                    err = json.dumps(ret)
                    raise CanNotCreateIndex(err)

        return indices_created

    def delete(self):
        """return number of indices closed
        """
        indices = select_indices(
            self.es,
            self.model.index_name_prefix,
            self.model.index_timestring,
            self.model.index_timestring_interval,
            self.model.delete.exec_offset + 1
        )

        indices_deleted = 0

        for index in indices:
            try:
                ret = curator.delete_indices(self.es, index)
                if ret is True:
                    indices_deleted += 1
                # elif ret is False: index doesn't exist

            except elasticsearch.exceptions.ConnectionTimeout as e:
                raise CanNotDeleteIndex(str(e))

        return indices_deleted

    def optimize(self):
        """return number of indices optimized
        Index optimization may takes a very long time if index size is huge( more than hundreds of GB).
        We must not block on this
        """
        indices = select_indices(
            self.es,
            self.model.index_name_prefix,
            self.model.index_timestring,
            self.model.index_timestring_interval,
            self.model.optimize.exec_offset
        )

        indices_optimized = 0

        for index in indices:
            # Attention: The following code will never returne sometimes and I don't know why,
            # so I set request_timeout to make sure it returns
            ret = curator.optimize_index(
                self.es,
                index,
                max_num_segments=self.model.optimize.target_segment_num,
                request_timeout=1200
            )

        return indices_optimized

    def snapshot(self):
        pass

    def replicate(self):
        """
        """
        indices = select_indices(
            self.es,
            self.model.index_name_prefix,
            self.model.index_timestring,
            self.model.index_timestring_interval,
            self.model.replicas.exec_offset

        )

        indices_replicated = 0

        for index in indices:
            try:
                ret = curator.change_replicas(self.es, index, replicas=self.model.replicas.target_replica_num)
            except elasticsearch.exceptions.ConnectionTimeout as e:
                raise CanNotReplicateIndex(str(e))

            if ret:
                indices_replicated += 1
            else:
                raise CanNotReplicateIndex("replicate error with " + str(index))

        return indices_replicated

    def relocate(self):
        """
        """
        indices = select_indices(
            self.es,
            self.model.index_name_prefix,
            self.model.index_timestring,
            self.model.index_timestring_interval,
            self.model.relocate.exec_offset,
        )

        target_allocation_config = eval(self.model.relocate.target_allocation_config)
        if not reset_allocation(self.es, indices):
            raise CanNotRelocateIndex("Can't initialize allocation configuration of the past")
        attributes = dict()
        for allocation_type in target_allocation_config:
            attributes[allocation_type] = dict()
            for attribute in target_allocation_config[allocation_type].split(','):
                key, value = attribute.split(':')
                value += ','
                if key in attributes[allocation_type]:
                    attributes[allocation_type][key] += value
                else:
                    attributes[allocation_type][key] = value

        for index in indices:
            for allocation_type in attributes:
                for attribute in attributes[allocation_type]:
                    try:
                        curator.allocation(
                            self.es,
                            indices=index,
                            rule="{0}={1}".format(attribute, attributes[allocation_type][attribute]),
                            allocation_type=allocation_type
                        )

                    except elasticsearch.exceptions.ConnectionTimeout as e:
                        raise CanNotRelocateIndex(str(e))
