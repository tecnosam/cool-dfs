# from client.client import Client
#
# m = Client('http://localhost:5000')
#
# res = m.upload_file('test-files/script', 'script')
# print(res)
# res = m.download_file(2)
# print(res)
import sys

from . import app
from .client import Client

if not sys.argv[1:]:
    net_url = input("Input network's URL")
else:
    net_url = sys.argv[1]

app.config['client'] = Client(net_url)

app.run(port=4000, debug=True)
