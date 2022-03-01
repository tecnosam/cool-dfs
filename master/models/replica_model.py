from master import db
from master.models.extras.generic_class import GenericModel
from datetime import datetime

from .extras.utils import delete_replica_data, delete_instance


class Replica(db.Model, GenericModel):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # offset = db.Column(db.Integer, nullable=False)  # offset in node storage blob
    partition_id = db.Column(db.Integer, db.ForeignKey('partition.id', ondelete='CASCADE'), nullable=False)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id', ondelete='CASCADE'), nullable=True)

    date_created = db.Column(db.DateTime, default=datetime.utcnow())


    preprocessors = {
        # 'offset': lambda x: x,
        'partition_id': lambda x: x,
        'node_id': lambda x: x,
    }

    def pop(self):
        _node = self.node
        delete_instance(self)
        delete_replica_data(self, _node)
        return self
