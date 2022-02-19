from flask import Flask
from flask_restful import Api

from .node import Node
from .config import master

import os

if not os.path.exists('storage'):
    os.mkdir('storage')

net_interface = Flask('node-manager')
net_interface.config['node'] = Node(master)

net_api = Api(net_interface)

import slave.resources


@net_interface.route('/')
def ping():
    return "Ping successful"
