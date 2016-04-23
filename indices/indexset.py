import json
import elasticsearch
import curator
from .exceptions import *
from .utils import indices_in_days, select_indices


class IndexSetObj(object):
    def __init__(self, model):
        self.model = model
        self.es = self.model.elasticsearch.client(timeout=120)

    def alias(self):
        pass

    def close(self):
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
                ret = curator.close_indices( self.es, indices )
            except elasticsearch.exceptions.ConnectionTimeout as e:
                raise CanNotCloseIndex(str(e))

        return indices_closed

    def create(self):
        import json

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

                if 'acknowledged' in ret and ret['acknowledged'] == True:
                    # {u'acknowledged': True}
                    indices_created += 1

                elif 'status' in ret and ret['status'] != 400:
                    err = json.dumps(ret)
                    raise CanNotCreateIndex(err)

        return indices_created

    def delete(self):
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
        indices = index_strategy.select_indices(
            self.es,
            self.model.index_name_prefix,
            self.model.index_timestring,
            self.model.index_timestring_interval,
            self.model.optimize.exec_offset
        )

        for index in indices:
            # Attention: The following code will never returne sometimes and I don't know why, so I set request_timeout to make sure it returns
            curator.optimize_index(self.es, index, max_num_segments=self.model.optimize.target_segment_num, request_timeout=1200)
            
    def snapshot(self):
        pass
