from .. import net_api

from .partition import PartitionResource


net_api.add_resource(PartitionResource, '/partitions', '/partitions/<int:replica_id>')
