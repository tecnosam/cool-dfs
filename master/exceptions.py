

class DuplicateKeyException(Exception):

    def __repr__(self):
        return super(DuplicateKeyException, self).__repr__()

    def __str__(self):
        return super(DuplicateKeyException, self).__str__()


class NoSuchInstance(Exception):

    def __repr__(self):
        return super(NoSuchInstance, self).__repr__()

    def __str__(self):
        return super(NoSuchInstance, self).__str__()
