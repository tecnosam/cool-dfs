

class NetReader:
    def __init__(self, byte_iter):
        super(NetReader, self).__init__()
        # Get list of generator objects and merge them together
        self.byte_list = list(byte_iter)
        pass

    def read(self):
        try:

            if self.byte_list[0] is None:
                self.byte_list.pop(0)
                return self.read()

            return next(self.byte_list[0])

        except StopIteration:
            self.byte_list.pop(0)
            return self.read()
        except IndexError:
            # there are no bytes in queue
            raise StopIteration()

    def __next__(self):
        return self.read()

    def __iter__(self):
        return self
