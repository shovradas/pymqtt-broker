import struct
from enum import Enum


class PacketType(Enum):
    CONNECT = 0x1
    CONNACK = 0x2
    PUBLISH = 0x3
    PUBACK = 0x4
    PUBREC = 0x5
    PUBREL = 0x6
    PUBCOMP = 0x7
    SUBSCRIBE = 0x8
    SUBACK = 0x9
    UNSUBSCRIBE = 0xA
    UNSUBACK = 0xB
    PINGREQ = 0xC
    PINGRESP = 0xD
    DISCONNECT = 0xE
    AUTH = 0xF


class Packet:
    def __init__(self, packet_type):
        self.packet_type = packet_type                     # 4 bits
        self.header_flags = 0b0000                         # 4 bits
        self.remaining_length = 0                          # 1-4 bytes # TODO: variable remaining lenght need to be implemented


class ConnectPacket(Packet):
    class ConnectFlags:
        def __init__(self):
            user_name = 0b0                                         # 1 bit
            password = 0b0                                          # 1 bit
            will_retain = 0b0                                       # 1 bit
            will_qos = 0b00                                         # 2 bits
            will_flag = 0b0                                         # 1 bit
            clean_start = 0b0                                       # 1 bit
            # reserved = 0b0

    # class Properties:
    #     def __init__(self):
    #         property_length = 0
    #         session_expiry_interval = 0
    #         receive_maximum = 0
    #         maximum_packet_size = 0
    #         topic_alias_maximum = 0
    #         request_response_information = 0
    #         request_problem_information = 0
    #         user_property = 0
    #         authentication_method = 0
    #         authentication_data = 0

    def __init__(self, protocol_name=None, protocol_version=None, connect_flags=None):
        super().__init__(PacketType.CONNECT)

        # variable header
        self.protocol_name = 'MQTT'.encode('utf-8')
        self.protocol_name_length = len(self.protocol_name)         # 2 bytes        
        self.protocol_version = 4                                   # 1 byte
        self.connect_flags = 2                                      # 1 byte
        self.keep_alive = 60                                        # 2 bytes

        # payload
        self.client_id = client_id.encode('utf-8')
        self.client_id_length = len(self.client_id)         # 2 bytes

    def encode(self):
        # TODO: variable remaining lenght need to be implemented
        format_without_header = f"H{self.protocol_name_length}sBBHH{self.client_id_length}s"
        self.remaining_length = struct.calcsize(format_without_header)

        format = f"!BB" + format_without_header
        packet = struct.pack(
            format,
            # header
            self.packet_type.value << 4,                    # control flag 0000
            self.remaining_length,
            # variable header
            self.protocol_name_length,
            self.protocol_name,
            self.protocol_version,
            self.connect_flags,
            self.keep_alive,
            # payload
            self.client_id_length,
            self.client_id
        )
        print(f"{format=}, {packet=}")
        return packet


class ConnAckPacket(Packet):
    def __init__(self, header_flags, remaining_length, connack_flags, reason_code):
        super().__init__(PacketType.CONNACK)
        self.header_flags = header_flags
        self.remaining_length = remaining_length
        # Variable Header
        self.connack_flags = connack_flags
        self.reason_code = reason_code

    def encode(self):
        self.remaining_length = 2

        format = f"!BBBB"
        packet = struct.pack(
            format,
            # header
            self.packet_type.value << 4,                    # control flag 0000
            self.remaining_length,
            # variable header
            self.connack_flags,
            self.reason_code
        )
        print(f"{format=}, {packet=}")
        return packet


class PublishPacket(Packet):
    def __init__(self, topic, message):
        super().__init__(PacketType.PUBLISH)

        # variable header
        self.topic = topic.encode('utf-8')
        self.topic_length = len(self.topic)                 # 2 bytes         

        # payload
        self.message = str(message).encode('utf-8')

    def encode(self):
        format_without_header = f"H{self.topic_length}s{len(self.message)}s"
        self.remaining_length = struct.calcsize(format_without_header)

        format = f"!BB" + format_without_header
        packet = struct.pack(
            format,
            # header
            self.packet_type.value << 4,                    # QoS = 0
            self.remaining_length,
            # variable header
            self.topic_length,
            self.topic,
            # payload
            self.message
        )
        print(f"{format=}, {packet=}")
        return packet


class SubscribePacket(Packet):
    def __init__(self, topic, messsage_id):
        super().__init__(PacketType.SUBSCRIBE)

        # variable header
        self.messsage_id = messsage_id                      # 2 bytes                

        # payload
        self.topic = topic.encode('utf-8')
        self.topic_length = len(self.topic)                 # 2 bytes
        self.qos = 0

    def encode(self):
        format_without_header = f"HH{self.topic_length}sB"
        self.remaining_length = struct.calcsize(format_without_header) # - 1 
        # TODO: Inspect remaining_length-1

        format = f"!BB" + format_without_header
        packet = struct.pack(
            format,
            # header
            (self.packet_type.value << 4) | 0b0010,
            self.remaining_length,
            # variable header
            self.messsage_id,
            # payload
            self.topic_length,
            self.topic,
            self.qos           
        )
        print(f"{format=}, {packet=}")
        return packet


class PingReqPacket(Packet):
    def __init__(self):
        super().__init__(PacketType.PINGREQ)
    
    def encode(self):
        format = f"!BB"
        packet = struct.pack(format,
            # header
            self.packet_type.value << 4,                    # control flag 0000
            self.remaining_length
            # variable header
            # payload
        )
        print(f"{format=}, {packet=}")
        return packet


class PingRespPacket(Packet):
    def __init__(self):
        super().__init__(PacketType.PINGRESP)
    
    def encode(self):
        format = f"!BB"
        packet = struct.pack(format,
            # header
            self.packet_type.value << 4,                    # control flag 0000
            self.remaining_length
            # variable header
            # payload
        )
        print(f"{format=}, {packet=}")
        return packet


class DisconnectPacket(Packet):
    def __init__(self):
        super().__init__(PacketType.DISCONNECT)
    
    def encode(self):
        remaining_length = 0

        format = f"!BB"
        packet = struct.pack(format,
            # header
            self.packet_type.value << 4,                    # control flag 0000
            remaining_length
            # variable header
            # payload
        )
        print(f"{format=}, {packet=}")
        return packet