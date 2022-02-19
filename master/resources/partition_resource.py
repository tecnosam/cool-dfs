from flask_restful import Resource, marshal_with, reqparse
from .all_fields import partition_fields
from .utils import exception_decorator

from master.models.partition_model import Partition
from master.exceptions import NoSuchInstance


class PartitionResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('file_id', required=True, type=int)
    parser.add_argument('offset', required=True, type=int)
    parser.add_argument('span', required=True, type=int)

    e_parser = reqparse.RequestParser()
    e_parser.add_argument('file_id', required=False, type=int)
    e_parser.add_argument('offset', required=False, type=int)
    e_parser.add_argument('span', required=False, type=int)

    @marshal_with(partition_fields)
    @exception_decorator(resource_name='partition')
    def get(self, partition_id: int = None):
        if partition_id is not None:
            _partition = Partition.query.get(partition_id)
            if _partition is None:
                raise NoSuchInstance('partition does not exist')
        return Partition.query.all()

    @marshal_with(partition_fields)
    @exception_decorator(resource_name='partition')
    def post(self, **_):
        pl = self.parser.parse_args(strict=True)
        print(pl)

        return Partition.add(**pl)

    # @marshal_with(partition_fields)
    # @exception_decorator(resource_name='partition')
    # def put(self, partition_id: int = None):
    #     pl = self.e_parser.parse_args(strict=True)
    #
    #     return Partition.edit(partition_id, **pl)

    @exception_decorator(resource_name='partition')
    def delete(self, partition_id: int = None):
        _partition = Partition.delete(partition_id)

        return {'id': _partition.id}
