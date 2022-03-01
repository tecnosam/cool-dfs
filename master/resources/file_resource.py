from flask_restful import Resource, marshal_with, reqparse
from flask import request
from .all_fields import file_fields
from .utils import exception_decorator, delete_partition_data

from master.models.file_model import File
from master.exceptions import NoSuchInstance


class FileResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str)
    parser.add_argument('mime', required=True, type=str)
    parser.add_argument('folder_id', required=False, type=int)
    parser.add_argument('client_id', required=True, type=int)

    e_parser = reqparse.RequestParser()
    e_parser.add_argument('name', required=False, type=str)
    e_parser.add_argument('mime', required=False, type=str)
    e_parser.add_argument('folder_id', required=False, type=int)
    e_parser.add_argument('client_id', required=False, type=int)

    @marshal_with(file_fields)
    @exception_decorator(resource_name='file')
    def get(self, file_id: int = None):
        if file_id is not None:
            _file = File.query.get(file_id)
            if _file is None:
                raise NoSuchInstance('file does not exist')
            return _file

        return File.query.all()

    @marshal_with(file_fields)
    @exception_decorator(resource_name='file')
    def post(self, **_):
        print('de', request.form)
        pl = self.parser.parse_args(strict=True)
        print(pl)

        return File.add(**pl)

    @marshal_with(file_fields)
    @exception_decorator(resource_name='file')
    def put(self, file_id: int = None):
        pl = self.e_parser.parse_args(strict=True)
        print(pl)

        return File.edit(file_id, **pl)

    @exception_decorator(resource_name='file')
    def delete(self, file_id: int = None):
        _file = File.delete(file_id)
        for partition in _file.partitions:
            delete_partition_data(partition)
        return {'id': _file.id, 'name': _file.name}
