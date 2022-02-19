from flask_restful import Resource, marshal_with, reqparse
from flask import request, abort, Response
from master.models.node_model import Node
from master.exceptions import NoSuchInstance

from .utils import exception_decorator
from .all_fields import node_fields


class NodeResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('protocol', required=True, type=str)
    # parser.add_argument('capacity', required=True, type=int)
    parser.add_argument('port', required=True, type=int)

    e_parser = reqparse.RequestParser()
    e_parser.add_argument('address', required=False, type=str)
    e_parser.add_argument('protocol', required=False, type=str)
    # e_parser.add_argument('capacity', required=False, type=int)
    e_parser.add_argument('port', required=False, type=int)

    @marshal_with(node_fields)
    @exception_decorator(resource_name='node', unique_key='address')
    def get(self):

        if 'all' in request.args:

            return Node.query.all()

        ip_address = request.args.get('address', request.remote_addr)
        _node = Node.query.filter_by(address=ip_address).first()

        if _node is None:
            abort(Response("You are not a node", 403))
        return _node

    @marshal_with(node_fields)
    @exception_decorator(resource_name='node', unique_key='address')
    def post(self):

        pl = self.parser.parse_args(strict=True)
        pl['address'] = request.remote_addr

        _node: Node = Node.query.filter_by(address=pl['address']).first()

        if _node is not None:
            _node.edit_self(**pl)
            return _node

        return Node.add(**pl)

    @marshal_with(node_fields)
    @exception_decorator(resource_name='node', unique_key='address')
    def put(self):

        _node: Node = Node.query.filter_by(address=request.remote_addr).first()
        if _node is None:
            raise NoSuchInstance("You aren't a node on this network")

        pl = self.e_parser.parse_args(strict=True)

        return _node.edit_self(**pl)

    @marshal_with(node_fields)
    @exception_decorator(resource_name='node', unique_key='address')
    def delete(self):

        _node: Node = Node.query.filter_by(address=request.remote_addr).first()

        return _node.pop()
