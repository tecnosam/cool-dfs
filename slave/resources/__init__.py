from .. import net_api

from .chunk import ChunkResource


net_api.add_resource(ChunkResource, '/chunks')
