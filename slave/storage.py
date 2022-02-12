from schema import Schema
from typing import Optional
from functools import reduce


class Storage:
    def __init__(self, node_id: str, capacity: int):
        self.node_id = node_id
        self.capacity = capacity
        self.schema = dict()

        self.format(b'\00')

    def dump_chunk(self, tag, data: bytes, **metadata: dict) -> Optional[Schema]:
        if tag in self.schema:
            return
            # todo: raise an exception

        free_frag = self._free_space(len(data))

        if free_frag is None:
            print("No free space")
            return

        self.write(free_frag[0], data)

        self.schema[tag] = Schema(tag=tag, pos=free_frag, **metadata)

        return self.schema[tag]

    def load_chunk(self, tag):
        if tag not in self.schema:
            return

        offset, span = self.schema[tag].pos

        with open(self.filename, 'rb') as f:
            f.seek(offset)
            data = reduce(lambda x, y: x+y, [f.read(1) for _ in range(span)])

        return data

    def free_chunk(self, tag):
        # we delete the metadata from schema, so it's block in storage is recognised as free space
        return self.schema.pop(tag)

    def expand(self, new_capacity):
        if new_capacity <= self.capacity:
            return

        self.write(new_capacity, bytes(new_capacity-self.capacity))
        self.capacity = new_capacity

        return self.capacity

    def format(self, byte: bytes):
        with open(self.filename, 'wb') as f:
            print("I'm running and i don't know why")
            f.write(byte * self.capacity)
        return

    def write(self, offset: int, data: bytes):
        with open(self.filename, 'rb+') as f:
            f.seek(offset, 0)
            f.write(data)

    def _free_space(self, size: int):
        n_chunks = len(self.schema)

        if not n_chunks:
            # if chunk is empty, just put it as the first chunk
            return (0, size) if size <= self.capacity else None

        values = sorted(list(self.schema.values()), key=lambda x: x.pos[0])
        values += [Schema(tag='end', pos=(self.capacity, 0))]

        # look for fragments between chunks
        for i in range(n_chunks):
            offset = sum(values[i].pos)  # start+span - 1 of current chunk

            space = values[i+1].pos[0] - offset  # start of next chunk - end of current chunk
            if size <= space:
                return offset, size

        return None

    @property
    def filename(self):
        return f'{self.node_id}.storage.net-machine'
