from master import db
from typing import List
from master.models.extras.generic_class import GenericModel

import requests


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

    @staticmethod
    def get_available_nodes(size: int, n_replicas):
        _nodes: List[Node] = Node.query.all()
        available_nodes = []
        for _node in _nodes:
            if len(available_nodes) == n_replicas:
                break

            if size < _node.free_space:
                available_nodes.append(_node)

        return available_nodes

    @property
    def free_space(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return int(response.text)
        return 0
