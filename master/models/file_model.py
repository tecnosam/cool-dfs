from master import db
from master.models.extras.generic_class import GenericModel
from datetime import datetime

from .extras.utils import delete_instance


class File(db.Model, GenericModel):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    mime = db.Column(db.String(100), unique=False, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id', ondelete='CASCADE'), nullable=True)

    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    partitions = db.relationship('Partition', backref='file')

    preprocessors = {
        'name': lambda x: x,
        'mime': lambda x: x,
        'client_id': lambda x: x,
        'folder_id': lambda x: x,
    }

    def pop(self):
        for partition in self.partitions:
            partition.pop()
        return delete_instance(self)
