from master import db
from master.models.extras.generic_class import GenericModel


class Replica(db.Model, GenericModel):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # offset = db.Column(db.Integer, nullable=False)  # offset in node storage blob
    partition_id = db.Column(db.Integer, db.ForeignKey('partition.id', ondelete='CASCADE'), nullable=False)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id', ondelete='CASCADE'), nullable=True)

    preprocessors = {
        # 'offset': lambda x: x,
        'partition_id': lambda x: x,
        'node_id': lambda x: x,
    }
