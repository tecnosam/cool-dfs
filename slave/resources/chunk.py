from flask_restful import Resource

from flask import request, Response, stream_with_context, abort

from .. import net_interface
import io


class ChunkResource(Resource):

    def get(self):
        node = net_interface.config['node']
        tag = request.args.get('tag')
        if tag:
            data: bytes = node.storage.load_chunk(tag)
            if data is None:
                abort(404)

            stream = io.BytesIO(data)

            return Response(stream_with_context(stream))

        return node.storage.schema.to_dict()

    def post(self):
        node = net_interface.config['node']
        raw = request.files['raw']

        schema = node.storage.dump_chunk(data=raw.stream, **dict(request.form))

        if schema is None:
            abort(Response("No space", 400))

        return schema.to_dict()
