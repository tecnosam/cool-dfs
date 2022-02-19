from client.client import Client

m = Client('http://localhost:5000')

# m.upload_file('main.py', 'script')
m.download_file(1)
