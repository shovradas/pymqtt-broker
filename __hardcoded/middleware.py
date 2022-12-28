from http import client
from struct import calcsize
from control_packets import *


class Encoder:
    def connect(self, packet: Packet):
        pass

    def connack(self, packet: Packet):
        pass

    def disconnect(self, packet: Packet):
        pass


class Decoder:
    def connect(self, data: bytes):
        header_flags = data[0] & 0b1111
        if header_flags == 0:
            remaining_length = data[1]
            # variable header
            protocol_name_length = int.from_bytes(data[2:4], byteorder='big')
            print(struct.unpack_from(f"!{protocol_name_length}sBBHH", data, 4))
                        
            format = f"!{protocol_name_length}sBBHH"
            protocol_name, protocol_version, connectflags, keep_alive, client_id_length = struct.unpack_from(format, data, 4)
            client_id = struct.unpack_from(f"{client_id_length}s", data, 4 + struct.calcsize(format))[0]
            print(f"{remaining_length=}, {protocol_name_length=}, {protocol_name=}, {protocol_version=}, {connectflags=}, {keep_alive=}, {client_id_length=} , {client_id=}")

            return ConnectPacket(str(client_id))
        else:
            pass # raise Malformed Packet Exception

    def connack(self, data: bytes):
        pass

    def disconnect(self, data: bytes):
        pass


class Middleware:
    def __init__(self, encoder=Encoder(), decoder=Decoder()) -> None:
        self.encoder = encoder
        self.decoder = decoder
        self.clients = []

    def encode(self, packet) -> bytes:
        encode_methods = {
            PacketType.CONNECT: self.encoder.connect,
            PacketType.CONNACK: self.encoder.connack,
            PacketType.DISCONNECT: self.encoder.disconnect,
        }
        return encode_methods[packet.packet_type](packet)

    def decode(self, data: bytes) -> Packet:
        packet_type = PacketType(data[0]>>4)
        decode_methods = {
            PacketType.CONNECT: self.decoder.connect,
            PacketType.CONNACK: self.decoder.connack,
            PacketType.DISCONNECT: self.decoder.disconnect,
        }
        return decode_methods[packet_type](data)
    
    def handle_request(self, data: bytes):
        packet_type = PacketType(data[0]>>4)
        packet = self.decode(data)
        if packet_type == PacketType.CONNECT:
            self.clients.append()
            return ConnAckPacket(0, 2, 0, 0).encode()
        elif packet_type == PacketType.PINGREQ:
            return PingRespPacket().encode()
        elif packet_type == PacketType.DISCONNECT:
            return DisconnectPacket().encode()
        else:
            return DisconnectPacket().encode()