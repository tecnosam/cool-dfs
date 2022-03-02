from flask import abort, Response
from flask_restful import marshal
from .all_fields import folder_fields
from requests import delete
from functools import wraps
from ..exceptions import DuplicateKeyException, NoSuchInstance


def prep_err(resource, status, msg, code):
    print(resource, status)
    abort(Response(msg, code))


def delete_replica_data(replica):
    _node = replica.node
    url = f"{_node.url}/partitions/{replica.id}"
    delete(url)


def delete_partition_data(partition):
    for _replica in partition.replicas:
        delete_replica_data(_replica)


class exception_decorator:
    def __init__(self, resource_name=None, unique_key=None):
        self.resource_name = resource_name
        self.unique_key = unique_key

    def __call__(self, func):
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):

            try:

                return func(*func_args, **func_kwargs)

            except DuplicateKeyException:
                unique_key = self.unique_key
                resource_name = self.resource_name

                if unique_key:
                    prep_err(resource_name, 'DUPLICATE KEY', f"record with {unique_key} exists", 400)
                else:
                    prep_err(resource_name, "DUPLICATE KEY", "key in form already belongs to an existing record", 400)

            except NoSuchInstance as e:

                resource_name = self.resource_name
                prep_err(resource_name, "NOT FOUND", str(e), 404)

        return wrapper
