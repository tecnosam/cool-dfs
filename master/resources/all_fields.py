from flask_restful import fields


replica_fields = {
    "id": fields.Integer,
    'partition': fields.Nested({
        'id': fields.Integer,
        'offset': fields.Integer,
        'span': fields.Integer
    }),
    "partition_id": fields.Integer,
    # "offset": fields.Integer,
    'node': fields.Nested({
        'id': fields.Integer,
        'url': fields.String
    }),
    "node_id": fields.Integer,
}

partition_fields = {
    'id': fields.Integer,
    'file': fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    }),
    'offset': fields.Integer,
    'span': fields.Integer,
    'replicas': fields.Nested(replica_fields),
}

file_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'folder': fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    }),
    'client': fields.Nested({
        'id': fields.Integer,
        'ip_address': fields.String
    }),
    'partitions': fields.Nested(partition_fields)
}

folder_fields = {
    'id': fields.Integer,
    'parent_id': fields.Integer,
    'name': fields.String,
    'client': fields.Nested({
        'id': fields.Integer,
        'ip_address': fields.String
    }),
    'parent_folder': fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    }),
    'sub_folders': fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    }),
    'files': fields.Nested(file_fields)
}

client_fields = {
    'id': fields.Integer,
    'ip_address': fields.String,
    'last_connect': fields.DateTime,
    'files': fields.Nested(file_fields),
    'folders': fields.Nested(folder_fields)
}

node_fields = {
    'id': fields.Integer,
    'protocol': fields.String,
    'address': fields.String,
    'port': fields.Integer,
    'url': fields.String,
    # 'capacity': fields.Integer,
    'replicas': fields.Nested(replica_fields)
}
