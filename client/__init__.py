from flask import Flask
from .client import Client

app = Flask(__name__)

from .resources import api
