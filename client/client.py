import requests
import os
import json
import magic
import concurrent.futures


class Client:
    def __init__(self, master: str):
        self.master_url = master
        self.mime = magic.Magic(mime=True)
        self.client_id = None  # todo this should be set when connected to master

    def upload_file(self, fn: str, net_dir: str):

        # send filename and desired directory to master to get tag
        server_file = self.new_file(fn)

        partitions = self.partition(fn)  # partition file into chunks

        # upload each chunk concurrently
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(self.process_partition, fn, partitions)

            for result in results:
                #
                if result.get('status'):
                    # send information about chunk to master node
                    # like what nodes contain the chunk
                    chunk_tag = result.get('chunk_tag')
                    replicas = result.get('nodes')
                    self.send_chunk_info(tag, chunk_tag, replicas)

        return results

    def send_chunk_info(self, tag, chunk_tag: str, replicas: list):
        json = {}

    def process_partition(self, fn, partition):
        node_urls = self.get_available_nodes(partition)

        return self.upload_chunk(fn, partition, node_urls)

    def new_file(self, fn, access_level: str = "PRIVATE"):
        metadata = {
            'real-name': fn, 'mime': self.mime.from_file(fn),
            'owner': self.client_id, 'access': access_level  # PRIVATE, PUBLIC OR SHARED
        }

        response = requests.post(f'{self.master_url}/new-file', data=metadata)

        return response.json()

    def get_available_nodes(self, partition: tuple) -> list:
        data = {"size": partition[1]}
        response = requests.post(f"{self.master_url}/available-nodes", data=data)

        return response.json()

    @staticmethod
    def upload_chunk(fn: str, partition: tuple, node_urls: list):
        tag = fn
        headers = {'tag': tag, 'nodes': node_urls, 'Content-Type': 'application/octet-stream'}

        with open(fn, 'rb') as f:
            f.seek(partition[0])
            data = f.read(partition[1])

        response = requests.post(f"{node_urls[0]}/upload-chunk", headers=headers, data=data)

        return response.json()

    @staticmethod
    def partition(fn: str, chunk_size: int = 134217728):
        size = os.path.getsize(fn)
        n_parts = (size // chunk_size)
        spill = size % chunk_size
        partitions = []

        for i in range(n_parts):
            offset = chunk_size * i
            span = (chunk_size * (i+1)) - offset
            part = (offset, span)
            partitions.append(part)

        if spill > 0:
            partitions.append((chunk_size*n_parts, spill))

        return partitions
