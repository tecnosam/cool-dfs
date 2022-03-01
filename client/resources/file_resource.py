from flask_restful import Resource, reqparse
from flask import request, Response, stream_with_context
from werkzeug.utils import secure_filename

from .. import app
from ..client import Client


class FileResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=False)
    parser.add_argument('folder_id', type=int, required=False)

    def get(self, file_id: int = None):
        client: Client = app.config['client']

        if file_id:
            if 'raw' in request.args:
                res = client.download_file(file_id)
                return Response(stream_with_context(res))

            return client.fetch_file_info(file_id)

        return client.fetch_file_info()

    def post(self, **_):
        client: Client = app.config['client']
        if 'file' in request.files:
            file = request.files['file']
            fn = secure_filename(file.filename)
            file.save(fn)
        else:
            fn = request.form['fn']

        name = request.form.get('name', fn)
        folder_id = request.form.get('folder_id', None)

        return client.upload_file(fn, name, folder_id)

    def put(self, file_id: int):
        # edit file, moving it to somewhere else or changing name
        client: Client = app.config['client']

        return client.edit_file(file_id, **self.parser.parse_args(strict=True))

    def delete(self, file_id: int):
        client: Client = app.config['client']

        return client.delete_file(file_id)
