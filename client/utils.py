import os


def file_size(fn: str):
    print(os.path.getsize(fn), fn, os.path.exists(fn))
    return os.path.getsize(fn)


def partition_file(fn: str, chunk_size: int = 134217728):
    size = file_size(fn)
    n_parts = (size // chunk_size)
    spill = size % chunk_size
    partitions = []
    print(size, n_parts, spill)

    for i in range(n_parts):
        offset = chunk_size * i
        span = (chunk_size * (i + 1)) - offset
        part = (offset, span)
        partitions.append(part)

    if spill > 0:
        partitions.append((chunk_size * n_parts, spill))

    return partitions


def generate_file(fn, size):
    chunk_size = 100*1024  # 100kb
    with open(fn, 'wb') as f:
        for _ in range(size // chunk_size):
            f.write(bytes(chunk_size))
        f.write(bytes(size % chunk_size))

    return


def read_partition(fn: str, offset: int, span: int, chunk_size: int = 8192):
    with open(fn, 'rb') as f:
        f.seek(offset)
        if span <= chunk_size:
            yield f.read(span)
            return
        n_chunks = span // chunk_size
        spill = span % chunk_size
        print("ded", n_chunks, spill)

        for _ in range(n_chunks):
            print(_)
            yield f.read(chunk_size)

        yield f.read(spill)

# def write_partition(fn: str, offset, data):
#     mode = 'rb+' if os.path.exists(fn) else 'wb'
#     with open(fn, mode) as f:
#         f.seek(offset)
#         if isinstance(data, bytes):
#             f.write(data)
#         elif isinstance(data, io.BufferedReader):
#             while byte := data.read(8192):
#                 f.write(byte)
#         else:
#             # it is a stream or iterator
#             for byte in data:
#                 f.write(byte)
#
#     return
