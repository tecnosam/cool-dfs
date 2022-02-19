from master import api, app

from .client_resource import ClientResource
from .file_resource import FileResource
from .folder_resource import FolderResource
from .node_resource import NodeResource
from .partition_resource import PartitionResource
from .replica_resource import ReplicaResource

from .additional_routes import *

api.add_resource(ClientResource, '/clients')
api.add_resource(NodeResource, '/nodes')
api.add_resource(FileResource, '/files', '/files/<int:file_id>')
api.add_resource(FolderResource, '/folders', '/folders/<int:folder_id>')
api.add_resource(PartitionResource, '/partitions', '/partitions/<int:partition_id>')
api.add_resource(ReplicaResource, '/replicas', '/replicas/<int:replica_id>')

api.init_app(app)
