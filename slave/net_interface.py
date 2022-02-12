import socket

from net_utils import setup_client_socket, setup_server_socket
from packet import Packet


class NetInterface:
    def __init__(self, node, interface_port: int):
        # reference to node object
        self.node = node

        # communication between master and node is through this socket
        self.master_channel = setup_client_socket(*node.master_node)

        # communication between client and node is through this socket
        self.client_interface = setup_server_socket(interface_port)

    @staticmethod
    def recv_packet(sock: socket.socket):
        size = int.from_bytes(sock.recv(64), 'big')  # 64-bit integer of size of packet
        return Packet.load(sock.recv(size))

    @staticmethod
    def send_packet(sock: socket.socket, packet: Packet):
        size, payload = packet.dump()
        sock.send(size)
        sock.send(payload)

    @staticmethod
    def send_response(sock: socket.socket, status: bool,data = None):
        # send status back to top
        response_packet = Packet({'type': 'response', 'status': status}, data)
        NetInterface.send_packet(sock, response_packet)

    def listen_to_clients(self):
        self.client_interface.listen()
        while True:
            client, address = self.client_interface.accept()

            print("Connected to client ", address)

            packet = self.recv_packet(client)

            if packet.header.get('type') == 'write':
                schema = self.process_write(packet)
                if schema is None:
                    # tell client that it could not store
                    self.send_response(client, False)
                    return

                next_nodes = packet.header['next_nodes']

                if len(next_nodes) >= 2:
                    next_nodes.pop(0)  # current node is popped
                    # if there are still nodes to write chunk to
                    next_socket = setup_client_socket(*next_nodes[0])
                    self.send_packet(next_socket, packet)

                    # receive response from next node
                    self.recv_packet(next_socket)  # todo do something with this
                    # todo: using the above, we need to tell the real client that this node does not
                    # todo: contain the data

                # send status back to top
                self.send_response(client, True)

            elif packet.header.get('type') == 'read':
                self.process_read(packet)  # load chunk into packet

                self.send_packet(client, packet)  # respond to client with updated packet

    def process_write(self, packet: Packet):
        data = packet.body
        tag = packet.header.get('tag')

        # todo: handle no space error

        schema = self.node.storage.dump_chunk(tag, data)

        # add offset to headers
        packet.header['offset'] = schema.pos[0]

        return schema

    def process_read(self, packet: Packet):
        tag = packet.header.get('tag')

        packet.body = self.node.storage.load_chunk(tag)
