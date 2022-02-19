from master import db
from master.models.extras.generic_class import GenericModel


class File(db.Model, GenericModel):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    mime = db.Column(db.String(100), unique=False, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id', ondelete='CASCADE'), nullable=True)

    partitions = db.relationship('Partition', backref='file', passive_deletes=True)

    preprocessors = {
        'name': lambda x: x,
        'mime': lambda x: x,
        'client_id': lambda x: x,
        'folder_id': lambda x: x,
    }
