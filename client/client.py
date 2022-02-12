import requests
import json
import magic
import concurrent.futures
from typing import List, Tuple
from utils import partition_file, file_size, generate_file, write_partition
import io


class Client:
    def __init__(self, master: str):
        self.master_url = master
        self.mime = magic.Magic(mime=True)
        self.client_id = None  # todo this should be set when connected to master

    def connect(self):
        self.client_id = 1

    def download_file(self, tag):
        # request file information from master node
        file = self.fetch_file_info(tag)

        generate_file(tag, file.get('size'))  # create a file with NULL-BYTES

        chunks = file.get('chunks', [])

        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = [executor.submit(self.download_chunk, tag, chunk) for chunk in chunks]

        return concurrent.futures.as_completed(result)

    def fetch_file_info(self, tag):
        # fetch file meta data
        return requests.get(f"{self.master_url}/files?tag={tag}").json()

    def upload_file(self, fn: str, tag: str):
        # Upload a file to Distributed File System

        file = self.create_new_file(fn, tag=tag, size=file_size(fn))

        partitions = partition_file(fn)  # partition file into chunks

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(self.process_partition, fn, part, file) for part in partitions]

        return concurrent.futures.as_completed(results)

    def create_new_file(self, fn, **metadata):
        # create new file in master node
        metadata = {'mime': self.mime.from_file(fn), 'owner': self.client_id, **metadata}

        response = requests.post(f'{self.master_url}/files', data=metadata)

        return response.json()

    def process_partition(self, fn: str, partition: Tuple[int, int], file: dict, n_replicas: int = 3):
        # fetch available nodes and send partition to that node
        node_urls = self.get_available_nodes(partition, n_replicas)

        partition_schema = self.upload_chunk(fn, file['tag'], partition, node_urls)

        return self.send_partition_info(file['id'], partition_schema)

    def get_available_nodes(self, partition: Tuple[int, int], n_replicas: int) -> list:
        # get list of available nodes that can store partition
        data = {"size": partition[1], 'n_replicas': n_replicas}

        response = requests.post(f"{self.master_url}/available-nodes", data=data)

        return response.json()

    def send_partition_info(self, file_id, partition_schema: dict):
        # send chunk/partition info to master to store
        data = json.dumps(partition_schema)

        response = requests.post(f"{self.master_url}/files/{file_id}", json=data)

        return response.json()

    @staticmethod
    def upload_chunk(fn: str, tag: str, partition: Tuple[int, int], node_urls: List[str]):
        # upload chunk to node
        data = {'tag': tag, 'offset': partition[0], 'nodes': node_urls}

        with open(fn, 'rb') as f:
            f.seek(partition[0])
            files = {"raw": io.BytesIO(f.read(partition[1]))}

        response = requests.post(f"{node_urls[0]}/chunks", data=data, files=files)

        return response.json()

    @staticmethod
    def download_chunk(fn: str, chunk: dict):
        # download chunk from source
        for node in chunk['nodes']:
            try:
                with requests.get(f"{node}/chunks?tag={chunk['tag']}") as r:
                    r.raise_for_status()
                    for inner_chunk in r.iter_content(chunk_size=8192):
                        write_partition(fn, chunk['offset'], inner_chunk)
                    return True  # since transfer was successful, we don't need the replicates
            except requests.exceptions.ConnectionError:
                continue  # transfer was not successful, so we move to the next replicate
            except requests.exceptions.RequestException:
                continue  # transfer was not successful, so we move on to the next replicate

        # it'll only get here if all replicates are unreachable
        return False
