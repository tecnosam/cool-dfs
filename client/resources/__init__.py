from flask_restful import Api
from .. import app

from .file_resource import FileResource
from .folder_resource import FolderResource

api = Api(app)

api.add_resource(FileResource, '/files', '/files/<int:file_id>')
api.add_resource(FolderResource, '/folders', '/folders/<int:folder_id>')

api.init_app(app)
