
import os


class Storage:
    def __init__(self, node_id: str):
        self.node_id = node_id

        # if (not os.path.exists(self.filename)) or clear:
        #     if capacity is None:
        #         raise TypeError('Storage expects a value for capacity if node_id is not found')
        #
        #     self.capacity = capacity
        #
        #     self.format(b'\00')
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)

    # def store_partition(self, i_stream, offset) -> bool:
    #     self.write(offset, i_stream)
    #
    #     return True

    # def read(self, offset, span) -> Optional[bytes]:
    #     # load bytes from blob storage
    #
    #     stream_chunk_size = 2048
    #
    #     with open(self.filename, 'rb') as f:
    #         f.seek(offset)
    #
    #         if span < stream_chunk_size:
    #             data = b''
    #             for _ in range(span//stream_chunk_size):
    #                 data += f.read(stream_chunk_size)
    #
    #             data += f.read(span % stream_chunk_size)
    #         else:
    #             data = f.read(span)
    #
    #     return data

    # def free_partition(self, tag):
    #     # we delete the metadata from metadata, so it's block in storage is recognised as free space
    #     if tag not in self.metadata:
    #         return None
    #     schema = self.metadata.pop(tag)
    #
    #     self.dump_schema()
    #     return schema

    # def expand(self, new_capacity):
    #     # Expand capacity of blob storage
    #     if new_capacity <= self.capacity:
    #         return
    #
    #     self.write(new_capacity, bytes(new_capacity-self.capacity))
    #     self.capacity = new_capacity
    #
    #     return self.capacity

    # def format(self, byte: bytes):
    #     # clear all bytes in raw file and assign them to param 'byte'
    #     with open(self.filename, 'wb') as f:
    #         print("Formatting new storage blob")
    #         chunk_size = 2097152  # 2 megabytes
    #         for _ in range(self.capacity // chunk_size):
    #             f.write(byte * chunk_size)
    #
    #         f.write(byte * (self.capacity % chunk_size))  # write spill
    #     return

    # def write(self, offset: int, data):
    #     with open(self.filename, 'rb+') as f:
    #         f.seek(offset, 0)
    #         if isinstance(data, bytes):
    #             f.write(data)
    #         else:
    #             while byte := data.read(2048):
    #                 f.write(byte)

    def write_file(self, fn: str, data):
        with open(f"{self.directory}/{fn}", 'wb') as f:
            if isinstance(data, bytes):
                f.write(data)
            else:
                while byte := data.read(2048):
                    f.write(byte)
        return True

    def read_file(self, fn) -> bytes:
        # load bytes from blob storage
        fn = f"{self.directory}/{fn}"
        if os.path.exists(fn):

            stream_chunk_size = 2048

            span = os.path.getsize(fn)

            with open(fn, 'rb') as f:

                if span < stream_chunk_size:
                    data = b''
                    for _ in range(span//stream_chunk_size):
                        data += f.read(stream_chunk_size)

                    data += f.read(span % stream_chunk_size)
                else:
                    data = f.read(span)

            return data

    def delete_file(self, fn):
        try:
            os.remove(f"{self.directory}/{fn}")
            return True
        except FileNotFoundError:
            return False
        except PermissionError:
            return False

    # def _free_space(self, size: int):
    #     # find free space in storage
    #     n_blocks = len(self.metadata)
    #
    #     if not n_blocks:
    #         # if chunk is empty, just put it as the first chunk
    #         return (0, size) if size <= self.capacity else None
    #
    #     values = sorted(list(self.metadata.values()), key=lambda x: x['pos'][0])
    #     values += [dict(tag='end', pos=(self.capacity, 0))]
    #
    #     # look for fragments between chunks
    #     for i in range(n_blocks):
    #         offset = sum(values[i]['pos'])  # start+span - 1 of current chunk
    #
    #         space = values[i+1]['pos'][0] - offset  # start of next chunk - end of current chunk
    #         if size <= space:
    #             return offset, size
    #
    #     return None

    # def load_schema(self):
    #     # load metadata from disk
    #     with open(f'storage/{self.node_id}.schema.net-machine', 'r') as f:
    #         return json.load(f)
    #
    # def dump_schema(self) -> None:
    #     # write metadata to disk
    #     with open(f'storage/{self.node_id}.schema.net-machine', 'w') as f:
    #         print(self.metadata)
    #         return json.dump({"capacity": self.capacity, "metadata": self.metadata}, f)

    # def set_metadata(self, schema):
    #     # property for setting metadata
    #     self.__metadata = schema
    #
    # def get_metadata(self):
    #     return self.__metadata

    # metadata = property(get_metadata, set_metadata)

    @property
    def filename(self):
        return f'storage/{self.node_id}.blob.net-machine'

    @property
    def directory(self):
        return f"storage/{self.node_id}-blob"
