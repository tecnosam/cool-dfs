import requests
import json
import magic
import concurrent.futures
from typing import Tuple
from .utils import partition_file, generate_file, write_partition
import io


class Client:
    def __init__(self, master: str):
        self.master_url = master
        self.mime = magic.Magic(mime=True)
        self.client_id = 1  # todo this should be set when connected to master

    def connect(self):
        self.client_id = 1

    def download_file(self, file_id):
        # request file information from master node
        file = self.fetch_file_info(file_id)

        size = sum([part['span'] for part in file['partitions']])

        generate_file(file['name'], size)  # create a file with NULL-BYTES

        partitions = file.get('partitions', [])

        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = [self.download_partition(file['name'], part) for part in partitions]
            # result = [executor.submit(self.download_partition, file['name'], part) for part in partitions]

        # return concurrent.futures.as_completed(result)
        return result

    def fetch_file_info(self, file_id):
        # fetch file meta data
        return requests.get(f"{self.master_url}/files/{file_id}").json()

    def upload_file(self, fn: str, name: str):
        # Upload a file to Distributed File System

        file = self.create_new_file(fn, name=name)

        partitions = partition_file(fn)  # partition_fields file into chunks
        print(partitions)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [self.process_partition(fn, part, file) for part in partitions]

        # return concurrent.futures.as_completed(results)
        return results

    def create_new_file(self, fn, **metadata):
        # create new file in master node
        metadata = {'mime': self.mime.from_file(fn), 'client_id': self.client_id, **metadata}
        print(metadata)

        response = requests.post(f'{self.master_url}/files', data=metadata)
        response.raise_for_status()

        return response.json()

    def process_partition(self, fn: str, partition: Tuple[int, int], file: dict, n_replicas: int = 1):
        # fetch available nodes and send partition_fields to that node
        print('init')
        nodes = self.__get_available_nodes(partition, n_replicas)

        partition = self.__upload_partition(file['id'], partition)

        # upload replicas to nodes
        replicas = self.__upload_replica(partition, nodes)

        self.__upload_replica_data(fn, partition, replicas)

        return partition

    def __upload_partition(self, file_id: int, partition: Tuple[int, int]):
        # upload chunk to node
        data = {'file_id': file_id, 'offset': partition[0], 'span': partition[1]}

        response = requests.post(f"{self.master_url}/partitions", data=data)
        print(response.text)
        response.raise_for_status()

        return response.json()

    def __upload_replica(self, partition, nodes):
        replicas = []
        for i in range(len(nodes)):
            node = nodes[i]
            data = {'node_id': node['id'], 'partition_id': partition['id']}
            response = requests.post(f"{self.master_url}/replicas", data=data)

            if response.status_code == 200:
                replicas.append(response.json())

        return replicas

    @staticmethod
    def __upload_replica_data(fn, partition, replicas: list):
        offset, span = partition['offset'], partition['span']

        with open(fn, 'rb') as f:
            f.seek(offset)

            files = {"raw": io.BytesIO(f.read(span))}

        replica = replicas.pop(0)
        node = replica['node']
        data = json.dumps(replicas)

        response = requests.post(f"{node['url']}/partitions/{replica['id']}", files=files, json=data)

        return response.json()

    @staticmethod
    def download_partition(fn: str, partition: dict):
        # download chunk from source
        for replica in partition['replicas']:
            print(replica)
            try:
                url = f"{replica['node']['url']}/partitions/{replica['id']}"  # url for node_url to access file
                with requests.get(url) as r:
                    r.raise_for_status()
                    for inner_chunk in r.iter_content(chunk_size=8192):
                        write_partition(fn, partition['offset'], inner_chunk)
                    return True  # since transfer was successful, we don't need the replicates
            except requests.exceptions.ConnectionError:
                continue  # transfer was not successful, so we move to the next replicate
            except requests.exceptions.RequestException:
                continue  # transfer was not successful, so we move on to the next replicate

        # it'll only get here if all replicates are unreachable
        return False

    def __get_available_nodes(self, partition: Tuple[int, int], n_replicas: int) -> list:
        # get list of available nodes that can store partition_fields
        data = {"size": partition[1], 'n_replicas': n_replicas}

        response = requests.post(f"{self.master_url}/available-nodes", data=data)

        return response.json()
