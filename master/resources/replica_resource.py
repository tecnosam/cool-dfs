from flask_restful import Resource, marshal_with, reqparse
from .all_fields import replica_fields
from .utils import exception_decorator

from master.models.replica_model import Replica
from master.exceptions import NoSuchInstance


class ReplicaResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('partition_id', required=True, type=int)
    parser.add_argument('node_id', required=True, type=int)
    # parser.add_argument('offset', required=True, type=int)

    e_parser = reqparse.RequestParser()
    e_parser.add_argument('partition_id', required=False, type=int)
    e_parser.add_argument('node_id', required=False, type=int)
    # e_parser.add_argument('offset', required=False, type=int)

    @marshal_with(replica_fields)
    @exception_decorator(resource_name='replica')
    def get(self, replica_id: int = None):

        if replica_id is not None:

            _replica = Replica.query.get(replica_id)

            if _replica is None:
                raise NoSuchInstance('replica does not exist')

        return Replica.query.all()

    @marshal_with(replica_fields)
    @exception_decorator(resource_name='replica')
    def post(self, **_):
        pl = self.parser.parse_args(strict=True)

        return Replica.add(**pl)

    # @marshal_with(replica_fields)
    # @exception_decorator(resource_name='replica')
    # def put(self, replica_id: int = None):
    #     pl = self.e_parser.parse_args(strict=True)
    #
    #     return Partition.edit(replica_id, **pl)

    @exception_decorator(resource_name='replica')
    def delete(self, replica_id: int = None):
        _replica = Replica.delete(replica_id)
        return {'id': _replica.id}
