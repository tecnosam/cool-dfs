
from .utils import push_instance, edit_instance, delete_instance


# noinspection PyArgumentList
class GenericModel:

    preprocessors = dict()

    @classmethod
    def add(cls, **kwargs):

        kwargs = {
            arg: cls.preprocessors[arg](kwargs[arg])
            for arg in kwargs if arg in cls.preprocessors
        }
        instance = cls(**kwargs)
        return push_instance(instance)

    @classmethod
    def edit(cls, prim_key, **kwargs):
        instance = cls.query.get(prim_key)
        return instance.edit_self(**kwargs)

    def edit_self(self, **kwargs):
        return edit_instance(self, kwargs, self.preprocessors)

    @classmethod
    def delete(cls, prim_key):
        instance = cls.query.get(prim_key)
        return delete_instance(instance)

    def pop(self):
        return delete_instance(self)
