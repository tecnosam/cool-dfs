# todo save data in schema to storage

class Schema:
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.kwargs = kwargs

    def to_json(self):
        return self.kwargs
