
from flask import request

from . import net_interface


@net_interface.route('/')
def ping():
    return "Ping successful"
