from elasticsearch import Elasticsearch
from .utils import indices_in_days, select_indices

class IndexSet(object):
    def __init__(self, model):
        self.model = model
        self.es = Elasticsearch(self.model.elasticsearch.address())

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

        if len( indices ) > 0:
            return curator.close_indices( self.es, indices )

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

        for index in indices:
            if not self.es.indices.exists(index):
                # ignore 400 cause by IndexAlreadyExistsException when creating an index
                self.es.indices.create(index=index, body=conf, ignore=400)

    def delete(self):
        # index deletion could be slow, set timeout to 60s
        indices = select_indices(
            self.es,
            self.model.index_name_prefix,
            self.model.index_timestring,
            self.model.index_timestring_interval,
            self.model.delete.exec_offset + 1
        )

        i = 0
        step = 2
        while i < len(indices):
            curator.delete_indices(self.es, indices[ i : i + step ])
            i += step

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
