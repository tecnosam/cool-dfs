from master import db
from master.models.extras.generic_class import GenericModel
from master.models.extras.utils import delete_instance
from datetime import datetime


class Folder(db.Model, GenericModel):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('folder.id', ondelete='CASCADE'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete='CASCADE'), nullable=False)

    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    files = db.relationship('File', backref='folder', passive_deletes=True)
    parent_folder = db.relationship(lambda: Folder, remote_side=id, backref='sub_folders', passive_deletes=True)

    preprocessors = {
        'name': lambda x: x,
        'parent_id': lambda x: x,
        'client_id': lambda x: x,
    }

    def pop(self):
        for _file in self.files:
            _file.pop()

        return delete_instance(self)
