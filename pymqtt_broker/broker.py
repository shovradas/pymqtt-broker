import socket
from threading import Thread
import time

from common import PacketType
from control_packets.connack_packet import ConnackPacket
from control_packets.simple_packets import DisconnectPacket, PingRespPacket
from control_packets.simple_packets import SubscribePacket
from control_packets.simple_packets import SubscribeAckPacket
from control_packets.connect_packet import ConnectPacket


class Client(Thread):
    def __init__(self, connection, address) -> None:
        super().__init__(daemon=True)

        self.connection = connection
        self.address = address
        self.id = None
        self.buffer = None

    def run(self) -> None:
        while True:
            try:
                self.buffer = self.connection.recv(2+256*1024*1024)
                print(f"[MQTT] {self.address[0]}:{self.address[1]} <- ({self.buffer})")
                
                if self.buffer:
                    packet = self.on_message()
                    
                    if not packet:
                        self.connection.close()
                        break
                    
                    response_buffer = packet.encode()
                    print(f"[MQTT] {self.address[0]}:{self.address[1]} -> ({response_buffer})")
                    self.connection.sendall(response_buffer)

                    if type(packet) == type(DisconnectPacket):
                        self.connection.close()
                        break

            except Exception as ex:
                # print('[ERROR]', ex)
                print("="*79); import traceback; traceback.print_exc(); print("="*79)
                self.connection.close()
                break

    def on_message(self):
        handle_func = {
            PacketType.CONNECT: self.on_connect,
            PacketType.PUBLISH: self.on_publish,
            PacketType.PUBACK: self.on_puback,
            PacketType.PUBREC: self.on_pubrec,
            PacketType.PUBREL: self.on_pubrel,
            PacketType.PUBCOMP: self.on_pubcomp,
            PacketType.SUBSCRIBE: self.on_subscribe,
            PacketType.UNSUBSCRIBE: self.on_unsubscribe,
            PacketType.PINGREQ: self.on_pingreq,
            PacketType.DISCONNECT: self.on_disconnect,
            PacketType.AUTH: self.on_auth
        }
        packet_type = PacketType(self.buffer[0]>>4); print(packet_type)
        if packet_type in handle_func.keys():
            return handle_func[packet_type]()
        return DisconnectPacket()
       
    def on_connect(self):
        packet = ConnectPacket.from_bytes(self.buffer)
        self.id = packet.payload.client_id
        return ConnackPacket(0, 2, 0, 0)

    def on_publish(self): pass
    def on_puback(self): pass
    def on_pubrec(self): pass
    def on_pubrel(self): pass
    def on_pubcomp(self): pass
    def on_subscribe(self): pass
    def on_unsubscribe(self): pass

    def on_pingreq(self):
        return PingRespPacket()

    def on_disconnect(self):
        return None

    def on_auth(self): pass


class Broker(Thread):
    def __init__(self, host='127.0.0.1', port=1883) -> None:
        super().__init__(daemon=True)
        self.host = host
        self.port = port
        self.clients = []
  
    def clean(self):
        while True:
            # print('Connected clients: [', ','.join([c.id for c in self.clients]), ']')
            for client in self.clients:
                if not client.is_alive():                    
                    client.join()
                    self.clients.remove(client)
            print('Connected clients: [', ','.join([c.id for c in self.clients]), ']')
            time.sleep(5)

    def run(self):
        Thread(target=self.clean, daemon=True).start()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Broker listening at {self.host}:{self.port}")
            while True:
                connection, client_address = s.accept()
                print(f"[TCP] Connected to {client_address[0]}:{client_address[1]}")

                client = Client(connection, client_address)
                client.start()
                self.clients.append(client)


if __name__ == '__main__':
    # broker = Broker('192.168.31.31')
    broker = Broker()
    broker.start()
    while True: continue