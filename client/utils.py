import os


def file_size(fn: str):
    return os.path.getsize(fn)


def partition_file(fn: str, chunk_size: int = 134217728):
    size = file_size(fn)
    n_parts = (size // chunk_size)
    spill = size % chunk_size
    partitions = []

    for i in range(n_parts):
        offset = chunk_size * i
        span = (chunk_size * (i + 1)) - offset
        part = (offset, span)
        partitions.append(part)

    if spill > 0:
        partitions.append((chunk_size * n_parts, spill))

    return partitions


def generate_file(fn, size):
    with open(fn, 'wb') as f:
        f.write(bytes(size))

    return


def write_partition(fn: str, offset, data):
    with open(fn, 'rb+') as f:
        f.seek(offset)
        f.write(data)
    return
