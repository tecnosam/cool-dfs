from flask import Flask
from flask_restful import Api

from node import Node

net_interface = Flask('node-manager')
net_interface.config['node'] = Node
net_api = Api(net_interface)

import resources


@net_interface.route('/')
def ping():
    return "Ping successful"
