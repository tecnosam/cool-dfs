from flask_restful import Resource, marshal_with, reqparse
from flask import request, abort, Response
from .all_fields import file_fields
from .utils import exception_decorator

from master.models.file_model import File
from master.models.client_model import Client
from master.exceptions import NoSuchInstance

from .. import db


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
        ip = request.remote_addr
        if file_id is not None:
            _file = File.query.get(file_id)
            if _file is None:
                raise NoSuchInstance('file does not exist')
            if _file.client.ip_address != ip:
                abort(Response("You don't have access to this file", 403))
            return _file

        client = Client.query.filter_by(ip_address=ip).first()
        if client is None:
            abort(Response("You are not registered client on this network", 403))

        return File.query.filter_by(client_id=client.id).all()

    @marshal_with(file_fields)
    @exception_decorator(resource_name='file')
    def post(self, **_):
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
        ip = request.remote_addr
        client = Client.query.filter_by(ip_address=ip).first()

        if client is None:
            abort(Response("You are not registered client on this network", 403))

        _file: File = File.query.filter_by(id=file_id, client_id=client.id).first()

        if _file is None:
            raise NoSuchInstance("file does not exist")

        _file = _file.pop()

        return {'id': _file.id, 'name': _file.name}
