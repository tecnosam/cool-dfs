import requests
import json
import magic
import concurrent.futures
from typing import Tuple
from .utils import partition_file, write_partition
import io
import os


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

        partitions = file.get('partitions', [])

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # result = [self.download_partition(file['name'], part) for part in partitions]
            name = file['name']
            print(partitions)
            result = [executor.submit(self.__download_partition, name, part) for part in partitions]
            # result = [self.__download_partition(name, part) for part in partitions]

        if all(concurrent.futures.as_completed(result)):
        # if all(result):
            partitions = sorted(partitions, key = lambda x: x['offset'])

            for partition in partitions:

                part_name = f"{file['name']}-{partition['id']}"

                write_partition(file['name'], partition['offset'], open(part_name, 'rb'))

                os.remove(part_name)

            return open(file['name'], 'rb')
        # return result

    def fetch_file_info(self, file_id: int = None):
        # fetch file meta data
        if file_id is not None:
            return requests.get(f"{self.master_url}/files/{file_id}").json()

        return requests.get(f"{self.master_url}/files").json()

    def upload_file(self, fn: str, name: str, folder_id: int = None):
        # Upload a file to Distributed File System

        file = self.__create_new_file(fn, name=name, folder_id=folder_id)

        partitions = partition_file(fn)  # partition_fields file into chunks

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # [self.__process_partition(fn, part, file) for part in partitions]
            result = [executor.submit(self.__process_partition, fn, part, file) for part in partitions]

        if all(concurrent.futures.as_completed(result)):
            return file

    def edit_file(self, file_id: int, **kwargs):
        file = requests.put(f"{self.master_url}/files/{file_id}", data=kwargs)
        file.raise_for_status()

        return file.json()

    def delete_file(self, file_id: int):
        file = requests.delete(f"{self.master_url}/files/{file_id}")
        file.raise_for_status()
        return file.json()

    def create_folder(self, name, parent_id: int = None):
        data = {'name': name, 'client_id': self.client_id, 'parent_id': parent_id}
        folder = requests.post(f"{self.master_url}/folders", data=data)
        folder.raise_for_status()

        return folder.json()

    def fetch_directory(self, folder_id: int = None):
        if folder_id is None:
            return requests.get(f"{self.master_url}/folders").json()
        return requests.get(f"{self.master_url}/folders/{folder_id}").json()

    def edit_folder(self, folder_id: int, **kwargs):
        folder = requests.put(f"{self.master_url}/folders/{folder_id}", data=kwargs)
        folder.raise_for_status()

        return folder.json()

    def delete_folder(self, folder_id: int = None):
        folder = requests.delete(f"{self.master_url}/folders/{folder_id}")
        folder.raise_for_status()

        return folder.json()

    def __create_new_file(self, fn, **metadata):
        # create new file in master node
        metadata = {'mime': self.mime.from_file(fn), 'client_id': self.client_id, **metadata}

        response = requests.post(f'{self.master_url}/files', data=metadata)
        response.raise_for_status()

        return response.json()

    def __process_partition(self, fn: str, partition: Tuple[int, int], file: dict, n_replicas: int = 1):
        # fetch available nodes and send partition_fields to that node
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
    def __download_partition(fn: str, partition: dict):
        # download chunk from source
        print("Starting download")
        part_id = partition['id']
        for replica in partition['replicas']:
            try:

                url = f"{replica['node']['url']}/partitions/{replica['id']}"  # url for node_url to access file

                with requests.get(url) as r:
                    r.raise_for_status()
                    # offset = 0
                    # for inner_chunk in r.iter_content(chunk_size=8192):
                        # write_partition(fn, partition['offset'], inner_chunk)
                    write_partition(f"{fn}-{part_id}", 0, r.iter_content(chunk_size=8192))
                    print("yessir")
                    # offset += 8192

                    return True  # since transfer was successful, we don't need the replicates

            except requests.exceptions.ConnectionError:
                print("con err")
                continue  # transfer was not successful, so we move to the next replicate

            except requests.exceptions.RequestException:
                print("Some exception")
                continue  # transfer was not successful, so we move on to the next replicate

        # it'll only get here if all replicates are unreachable
        return False

    def __get_available_nodes(self, partition: Tuple[int, int], n_replicas: int) -> list:
        # get list of available nodes that can store partition_fields
        data = {"size": partition[1], 'n_replicas': n_replicas}

        response = requests.post(f"{self.master_url}/available-nodes", data=data)

        return response.json()
