from flask_restful import Resource, reqparse

from .. import app
from ..client import Client


class FolderResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Name of the folder you want to create")
    parser.add_argument('parent_id', type=int, required=False)

    eparser = reqparse.RequestParser()
    eparser.add_argument('name', type=str, required=False)
    eparser.add_argument('parent_id', type=int, required=False)

    def get(self, folder_id: int = None):
        client: Client = app.config['client']

        if folder_id:

            return client.fetch_directory(folder_id)

        return client.fetch_directory()

    def post(self, **_):
        client: Client = app.config['client']

        return client.create_folder(**self.parser.parse_args(strict=True))

    def put(self, folder_id: int):
        # edit file, moving it to somewhere else or changing name
        client: Client = app.config['client']

        return client.edit_folder(folder_id, **self.eparser.parse_args(strict=True))

    def delete(self, folder_id: int):
        client: Client = app.config['client']

        return client.delete_folder(folder_id)
