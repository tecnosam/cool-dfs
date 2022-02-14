from flask_restful import Resource

from flask import request, Response, stream_with_context, abort

from .. import net_interface
import io


class ChunkResource(Resource):

    def get(self):
        node = net_interface.config['node']
        tag = request.args.get('tag')
        if tag:

            if 'metadata' in request.args:
                # if the user just wants the metadata
                schema = node.storage.metadata.get(tag)

                if schema is None:
                    # null checks on metadata
                    abort(Response("Tag not found", 404))

                return schema

            data: bytes = node.storage.load_chunk(tag)

            if data is None:
                # null check on bytes
                abort(Response("Tag not found", 404))

            stream = io.BytesIO(data)

            return Response(stream_with_context(stream))

        return node.storage.metadata

    def post(self):
        try:
            node = net_interface.config['node']
            raw = request.files.get('raw')

            if raw is None:
                abort(Response("You need to parse the raw data as a file", 400))

            if 'tag' not in request.form:
                abort(Response("You need to parse a tag field in the form body", 400))
            if 'data_size' not in request.form:
                abort(Response("You need to parse the length of data in bytes in form body", 400))

            schema = node.storage.dump_chunk(i_stream=raw.stream, **dict(request.form))

            if schema is None:
                abort(Response("No space", 400))

            return schema
        except FileExistsError as e:
            abort(Response(str(e), 400))

    def delete(self):
        node = net_interface.config['node']
        tag = request.args.get('tag', '')

        schema = node.storage.free_chunk(tag)
        if schema is None:
            abort(Response("Tag not found", 404))

        return schema
