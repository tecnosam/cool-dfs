from master import db
from master.models.extras.generic_class import GenericModel


class Partition(db.Model, GenericModel):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id', ondelete='CASCADE'), nullable=False)
    offset = db.Column(db.Integer, nullable=False)
    span = db.Column(db.Integer, nullable=False)

    replicas = db.relationship('Replica', backref='partition', passive_deletes=True)

    preprocessors = {
        'file_id': lambda x: x,
        'offset': lambda x: x,
        'span': lambda x: x,
    }
