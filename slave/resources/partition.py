import json

from flask_restful import Resource

from flask import request, Response, stream_with_context, abort

from .. import net_interface
import io
import requests


class PartitionResource(Resource):

    def get(self, replica_id: int):
        node = net_interface.config['node']
        # offset = int(request.args.get('offset'))
        # span = int(request.args.get('span'))

        data: bytes = node.storage.read_file(f"replica-{replica_id}")

        stream = io.BytesIO(data)

        return Response(stream_with_context(stream))

    def post(self, replica_id: int):
        _node = net_interface.config['node']

        raw = request.files.get('raw')

        if raw is None:
            abort(Response("You need to parse the raw data as a file", 400))

        status = _node.storage.write_file(f'replica-{replica_id}', raw)

        replicas = request.get_json()
        if replicas:
            self.forward_replica(replicas, raw.stream)

        return {"success": status}

    @staticmethod
    def forward_replica(replicas, stream):
        replica = replicas.pop(0)
        node = replica['node']

        files = {'raw': stream}
        data = json.dumps(replica)

        response = requests.post(f"{node['url']}/partitions/{replica['id']}", files=files, json=data)

        return response.json()

    def delete(self, replica_id: int):
        node = net_interface.config['node']

        status = node.storage.delete_file(f"replica-{replica_id}")

        return {'success': status}
