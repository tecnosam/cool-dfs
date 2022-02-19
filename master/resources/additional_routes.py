from .. import app

from flask import jsonify

from flask_restful import reqparse, marshal

from master.models.node_model import Node
from .all_fields import node_fields


@app.route('/available-nodes', methods=['POST'])
def available_nodes():
    parser = reqparse.RequestParser()
    parser.add_argument('size', type=int, required=True)
    parser.add_argument('n_replicas', type=int, default=1)

    pl = parser.parse_args(strict=True)
    nodes = marshal(Node.get_available_nodes(**pl), node_fields)

    return jsonify(nodes)
