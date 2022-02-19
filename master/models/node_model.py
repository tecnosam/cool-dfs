from master import db
from typing import List
from master.models.extras.generic_class import GenericModel


class Node(db.Model, GenericModel):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    protocol = db.Column(db.String, default='http')
    address = db.Column(db.String(100), unique=True, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    # capacity = db.Column(db.Integer, nullable=False)

    replicas = db.relationship('Replica', backref='node', passive_deletes=True)

    preprocessors = {
        'address': lambda x: x,
        'port': lambda x: x,
        # 'capacity': lambda x: x,
    }

    @property
    def url(self):
        return f"{self.protocol}://{self.address}:{self.port}"

    # def free_space(self, size: int):
    #     # find free space in storage
    #     n_blocks = len(self.replicas)
    #
    #     if not n_blocks:
    #         # if chunk is empty, just put it as the first chunk
    #         return (0, size) if size <= self.capacity else None
    #
    #     values = sorted(self.replicas, key=lambda x: x.offset)
    #     values += [dict(tag='end', pos=(self.capacity, 0))]
    #
    #     # look for fragments between chunks
    #     for i in range(n_blocks):
    #         offset = values[i].offset + values[i].partition.span  # start+span - 1 of current chunk
    #
    #         space = values[i+1].offset - offset  # start of next chunk - end of current chunk
    #         if size <= space:
    #             return offset
    #
    #     return None

    @staticmethod
    def get_available_nodes(size: int, n_replicas):
        _nodes: List[Node] = Node.query.all()
        available_nodes = []
        for _node in _nodes:
            if len(available_nodes) == n_replicas:
                break

            # todo: check if node has space to accomodate size
            print(size)
            available_nodes.append(_node)

        return available_nodes
