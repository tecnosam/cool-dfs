import json

from typing import Optional
import os


class Storage:
    def __init__(self, node_id: str, capacity: int = None, clear: bool = False):
        self.node_id = node_id

        if (not os.path.exists(self.filename)) or clear:
            if capacity is None:
                raise TypeError('Storage expects a value for capacity if node_id is not found')

            self.capacity = capacity

            self.format(b'\00')

            self.metadata = dict()
            self.dump_schema()

        else:
            data = self.load_schema()

            self.capacity: int = data['capacity']

            self.__metadata: dict = data['metadata']

    def dump_chunk(self, tag, i_stream, data_size: int, **metadata: dict) -> Optional[dict]:
        # store bytes in blob storage, and save its meta data
        if tag in self.metadata:
            raise FileExistsError(1, 'Tag allocated', 'Block with tag exists')

        data_size = int(data_size)

        free_frag = self._free_space(data_size)

        if free_frag is None:
            print("No free space")
            return

        self.write(free_frag[0], i_stream)

        self.metadata[tag] = dict(tag=tag, pos=free_frag, **metadata)
        self.dump_schema()

        return self.metadata[tag]

    def load_chunk(self, tag) -> Optional[bytes]:
        # load bytes from blob storage
        if tag not in self.metadata:
            return

        offset, span = self.metadata[tag]['pos']

        stream_chunk_size = 2048

        with open(self.filename, 'rb') as f:
            f.seek(offset)

            if span < stream_chunk_size:
                data = b''
                for _ in range(span//stream_chunk_size):
                    data += f.read(stream_chunk_size)

                data += f.read(span % stream_chunk_size)
            else:
                data = f.read(span)

        return data

    def free_chunk(self, tag):
        # we delete the metadata from metadata, so it's block in storage is recognised as free space
        if tag not in self.metadata:
            return None
        schema = self.metadata.pop(tag)

        self.dump_schema()
        return schema

    def expand(self, new_capacity):
        # Expand capacity of blob storage
        if new_capacity <= self.capacity:
            return

        self.write(new_capacity, bytes(new_capacity-self.capacity))
        self.capacity = new_capacity

        return self.capacity

    def format(self, byte: bytes):
        # clear all bytes in raw file and assign them to param 'byte'
        with open(self.filename, 'wb') as f:
            print("Formatting new storage blob")
            chunk_size = 2097152  # 2 megabytes
            for _ in range(self.capacity // chunk_size):
                f.write(byte * chunk_size)

            f.write(byte * (self.capacity % chunk_size))  # write spill
        return

    def write(self, offset: int, data):
        with open(self.filename, 'rb+') as f:
            f.seek(offset, 0)
            if isinstance(data, bytes):
                f.write(data)
            else:
                while byte := data.read(2048):
                    f.write(byte)

    def _free_space(self, size: int):
        # find free space in storage
        n_chunks = len(self.metadata)

        if not n_chunks:
            # if chunk is empty, just put it as the first chunk
            return (0, size) if size <= self.capacity else None

        values = sorted(list(self.metadata.values()), key=lambda x: x['pos'][0])
        values += [dict(tag='end', pos=(self.capacity, 0))]

        # look for fragments between chunks
        for i in range(n_chunks):
            offset = sum(values[i]['pos'])  # start+span - 1 of current chunk

            space = values[i+1]['pos'][0] - offset  # start of next chunk - end of current chunk
            if size <= space:
                return offset, size

        return None

    def load_schema(self):
        # load metadata from disk
        with open(f'storage/{self.node_id}.schema.net-machine', 'r') as f:
            return json.load(f)

    def dump_schema(self) -> None:
        # write metadata to disk
        with open(f'storage/{self.node_id}.schema.net-machine', 'w') as f:
            print(self.metadata)
            return json.dump({"capacity": self.capacity, "metadata": self.metadata}, f)

    def set_metadata(self, schema):
        # property for setting metadata
        self.__metadata = schema

    def get_metadata(self):
        return self.__metadata

    metadata = property(get_metadata, set_metadata)

    @property
    def filename(self):
        return f'storage/{self.node_id}.blob.net-machine'
