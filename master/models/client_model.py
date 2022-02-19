from master import db
from datetime import datetime
from master.models.extras.generic_class import GenericModel


class Client(db.Model, GenericModel):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(100), unique=True, nullable=False)

    last_connect = db.Column(db.DateTime, default=datetime.utcnow())

    files = db.relationship('File', backref='client', passive_deletes=True)
    folders = db.relationship('Folder', backref='client', passive_deletes=True)

    preprocessors = {
        'ip_address': lambda x: x
    }
