from flask_restful import Resource, marshal_with, marshal, reqparse
from flask import request
from master.models.folder_model import Folder
from master.models.file_model import File
from master.exceptions import NoSuchInstance
from .all_fields import folder_fields, file_fields
from .utils import exception_decorator, delete_partition_data


class FolderResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str)
    parser.add_argument('parent_id', required=False, type=int, default=None)
    parser.add_argument('client_id', required=True, type=int)

    e_parser = reqparse.RequestParser()
    e_parser.add_argument('name', required=False, type=str)
    e_parser.add_argument('parent_id', required=False, type=int)
    # e_parser.add_argument('client_id', required=False, type=int)

    @exception_decorator(resource_name='folder')
    def get(self, folder_id=None):
        client_id = request.args['client_id']

        if folder_id is not None:

            _folder = Folder.query.filter_by(id=folder_id, client_id=client_id).first()

            if _folder is None:
                raise NoSuchInstance("No such folder with ID %d" % folder_id)

            return marshal(_folder, folder_fields)

        elif 'full-root' in request.args:
            files = File.query.filter_by(folder_id=None, client_id=client_id).all()
            folders = Folder.query.filter_by(parent_id=None, client_id=client_id).all()

            _folder = {'files': marshal(files, file_fields), 'sub_folders': marshal(folders, folder_fields)}

        else:
            _folder = Folder.query.filter_by(client_id=client_id).all()
            _folder = marshal(_folder, folder_fields)

        return _folder

    @marshal_with(folder_fields)
    @exception_decorator(resource_name='folder')
    def post(self, **_):
        pl = self.parser.parse_args(strict=True)
        return Folder.add(**pl)

    @marshal_with(folder_fields)
    @exception_decorator(resource_name='folder')
    def put(self, folder_id=None):
        pl = self.e_parser.parse_args(strict=True)
        return Folder.edit(folder_id, **pl)

    @exception_decorator(resource_name='folder')
    def delete(self, folder_id=None):

        client_id = request.args['client_id']
        _folder = Folder.query.filter_by(id=folder_id, client_id=client_id).first()
        if _folder is None:
            raise NoSuchInstance("Folder does not exist")

        _folder = _folder.pop()

        return {'id': _folder.id}
