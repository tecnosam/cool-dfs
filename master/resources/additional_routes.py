from .. import app

from flask import jsonify

from flask_restful import reqparse, marshal

from master.models.node_model import Node
from master.models.file_model import File
from master.models.folder_model import Folder
from .all_fields import node_fields, file_fields, folder_fields


@app.route('/available-nodes', methods=['POST'])
def available_nodes():
    parser = reqparse.RequestParser()
    parser.add_argument('size', type=int, required=True)
    parser.add_argument('n_replicas', type=int, default=1)

    pl = parser.parse_args(strict=True)
    nodes = marshal(Node.get_available_nodes(**pl), node_fields)

    return jsonify(nodes)


@app.route("/root")
def tree():
    files = File.query.filter_by(folder_id=None).all()
    folders = Folder.query.filter_by(parent_id=None).all()

    return jsonify({'files': marshal(files, file_fields), 'sub_folders': marshal(folders, folder_fields)})
