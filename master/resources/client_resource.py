import datetime

from flask_restful import Resource, marshal_with
from flask import request
from master.models.client_model import Client
from .utils import exception_decorator
from .all_fields import client_fields


class ClientResource(Resource):

    @marshal_with(client_fields)
    @exception_decorator(resource_name='client', unique_key='ip_address')
    def get(self):

        if 'use_ip' in request.args:
            ip_address = request.args.get('ip_address', request.remote_addr)
            return Client.query.filter_by(ip_address=ip_address)
        return Client.query.all()

    @marshal_with(client_fields)
    @exception_decorator(resource_name='client', unique_key='ip_address')
    def post(self):
        ip_address = request.remote_addr

        _client: Client = Client.query.filter_by(ip_address=ip_address).first()
        if not _client:
            _client = Client.add(ip_address=ip_address)
        else:
            _client.edit_self(last_connect=datetime.datetime.utcnow())

        return _client
