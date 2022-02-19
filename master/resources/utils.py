from flask import abort, Response
from functools import wraps
from ..exceptions import DuplicateKeyException, NoSuchInstance


def prep_err(resource, status, msg, code):
    print(resource, status)
    abort(Response(msg, code))


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
