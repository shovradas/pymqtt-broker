import struct
from common import PacketType
from common import VariableByteInteger
from control_packets.properties import Properties
from control_packets.properties import PropertyValueType


class Packet:
    def __init__(self, packet_type, header_flags) -> None:
        self.packet_type = packet_type                                          # 4 bits
        self.header_flags = header_flags                                        # 4 bits

    def encode(self):
        if not hasattr(self, 'remaining_length'):
            raise Exception('Can not encode without REMAINING LENGTH')

        first_byte = (self.packet_type.value << 4) | self.header_flags
        buffer = bytearray([first_byte])
        buffer += self.remaining_length.bytes
        return buffer

    @classmethod
    def from_bytes(cls, buffer):
        packet_type = PacketType(buffer[0] >> 4)
        header_flags = buffer[0] % 16 # TODO: check if 16 is correct

        obj = cls(packet_type, header_flags)
        obj.remaining_length = VariableByteInteger.from_bytes(buffer, offset=1)
        return obj


class PublishPacket(Packet):
    def __init__(self, topic_name, packet_identifier, properties=None, packet_type=PacketType.PUBLISH, header_flags=0b0000) -> None:
        super().__init__(packet_type, header_flags)
        # Variable-Header
        self.topic_name = topic_name
        self.packet_identifier = packet_identifier
        self.properties = properties
        # Payload
        


class SubscribePacket(Packet):
    def __init__(self, packet_identifier, topic_filters, properties=None, packet_type=PacketType.SUBACK, header_flags=0b0010) -> None:
        super().__init__(packet_type, header_flags)
        # Variable-Header
        self.packet_identifier = packet_identifier
        self.properties = properties
        # Payload
        self.topic_filters = topic_filters # (topic, option)

    def encode(self):
        buffer = bytearray()
        buffer += self.packet_identifier.to_bytes(2, 'big')
        buffer += self.properties.encode()

        for tf in self.topic_filters:
            buffer += len(tf[0]).to_bytes(2, 'big')
            buffer += tf[0].encode('utf-8')
            buffer += tf[1].to_bytes(1, 'big')

        self.remaining_length = VariableByteInteger(len(buffer))
        buffer = super().encode() + buffer
      
        return buffer

    @classmethod
    def from_bytes(cls, buffer):
        fixed_header = Packet.from_bytes(buffer)
        offset = 1 + fixed_header.remaining_length.bytes_count

        # Variable-Header
        packet_identifier = int.from_bytes(buffer[offset:offset+2], byteorder='big')
        offset += 2
        
        properties = Properties.from_bytes(fixed_header.packet_type, buffer, offset)
        offset += properties.property_length.bytes_count + properties.property_length.value
        
        # Payload
        end = len(buffer)
        topic_filters = []
        while offset<end:
            topic_length = int.from_bytes(buffer[offset:offset+2], byteorder='big')
            offset += 2

            topic = buffer[offset:offset+topic_length].decode('utf-8')
            offset += topic_length
            
            options = buffer[offset]
            offset += 1

            topic_filters.append((topic, options))

        return cls(packet_identifier, topic_filters, properties, fixed_header.packet_type, fixed_header.header_flags)


class SubscribeAckPacket(Packet):
    def __init__(self, packet_identifier, properties=None, reason_codes=[], packet_type=PacketType.SUBACK, header_flags=0b0000) -> None:
        super().__init__(packet_type, header_flags)
        # Variable-Header
        self.packet_identifier = packet_identifier
        self.properties = properties
        # Payload
        self.reason_codes = reason_codes

    def encode(self):
        buffer = bytearray()
        # Variable-Header
        buffer += self.packet_identifier.to_bytes(2, 'big')
        buffer += self.properties.encode()
        # Payload
        for reason_code in self.reason_codes:        
            buffer += reason_code.to_bytes(1, 'big')

        self.remaining_length = VariableByteInteger(len(buffer))
        return super().encode() + buffer

    @classmethod
    def from_bytes(cls, buffer):
        fixed_header = Packet.from_bytes(buffer)
        offset = 1 + fixed_header.remaining_length.bytes_count

        # Variable-Header
        packet_identifier = int.from_bytes(buffer[offset:offset+2], byteorder='big')
        offset += 2
        
        properties = Properties.from_bytes(fixed_header.packet_type, buffer, offset)
        offset += properties.property_length.bytes_count + properties.property_length.value

        # Payload
        end = len(buffer)
        reason_codes = []
        while offset<end:
            reason_codes.append(buffer[offset])
            offset += 1

        return cls(packet_identifier, properties, reason_codes, fixed_header.packet_type, fixed_header.header_flags)


class UnsubscribePacket(Packet):
    def __init__(self, packet_identifier, topic_filters, properties=None, packet_type=PacketType.UNSUBSCRIBE, header_flags=0b0010) -> None:
        super().__init__(packet_type, header_flags)
        # Variable-Header
        self.packet_identifier = packet_identifier
        self.properties = properties
        # Payload
        self.topic_filters = topic_filters

    def encode(self):
        buffer = bytearray()
        buffer += self.packet_identifier.to_bytes(2, 'big')
        buffer += self.properties.encode()

        for tf in self.topic_filters:
            encoded_tf = tf.encode('utf-8')
            buffer += len(encoded_tf).to_bytes(2, 'big')
            buffer += encoded_tf

        self.remaining_length = VariableByteInteger(len(buffer))
        buffer = super().encode() + buffer
      
        return buffer

    @classmethod
    def from_bytes(cls, buffer):
        fixed_header = Packet.from_bytes(buffer)
        offset = 1 + fixed_header.remaining_length.bytes_count

        # Variable-Header
        packet_identifier = int.from_bytes(buffer[offset:offset+2], byteorder='big')
        offset += 2
        
        properties = Properties.from_bytes(fixed_header.packet_type, buffer, offset)
        offset += properties.property_length.bytes_count + properties.property_length.value
        
        # Payload
        end = len(buffer)
        topic_filters = []
        while offset<end:
            topic_length = int.from_bytes(buffer[offset:offset+2], byteorder='big')
            offset += 2

            topic = buffer[offset:offset+topic_length].decode('utf-8')
            offset += topic_length

            topic_filters.append(topic)

        return cls(packet_identifier, topic_filters, properties, fixed_header.packet_type, fixed_header.header_flags)

        
class UnsubAckPacket(SubscribeAckPacket):
    def __init__(self, packet_identifier, properties=None, reason_codes=[], packet_type=PacketType.UNSUBACK, header_flags=0b0000) -> None:
        super().__init__(packet_identifier, properties, reason_codes, packet_type, header_flags)    


class PingReqPacket(Packet):
    def __init__(self, packet_type=PacketType.PINGREQ, header_flags=0b0000) -> None:
        super().__init__(packet_type, header_flags)
        self.remaining_length = 0

    @classmethod
    def from_bytes(cls, buffer):    
        fixed_header = Packet.from_bytes(buffer)
        return cls(fixed_header.packet_type, fixed_header.header_flags)


class PingRespPacket(Packet):
    def __init__(self, packet_type=PacketType.PINGRESP, header_flags=0b0000) -> None:
        super().__init__(packet_type, header_flags)
        self.remaining_length = 0

    @classmethod
    def from_bytes(cls, buffer):    
        fixed_header = Packet.from_bytes(buffer)
        return cls(fixed_header.packet_type, fixed_header.header_flags)


class DisconnectPacket(Packet):
    def __init__(self, packet_type=PacketType.DISCONNECT, header_flags=0b0000, reason_code=None, properties=None):
        super().__init__(packet_type, header_flags)
        # Variable Header
        self.reason_code = reason_code
        self.properties = properties
    
    def encode(self):       
        buffer = bytearray()
        if self.reason_code:
            buffer += bytes([self.reason_code])
            if self.properties:
                buffer += self.properties.encode()
        
        self.remaining_length = len(buffer)        
        return super().encode() + buffer

    @classmethod
    def from_bytes(cls, buffer):
        fixed_header = Packet.from_bytes(buffer)

        obj = cls(fixed_header.packet_type, fixed_header.header_flags)

        if fixed_header.remaining_length.value:
            offset = 1 + fixed_header.remaining_length.bytes_count

            obj.reason_code = buffer[offset]
            offset += 1

            obj.properties = Properties.from_bytes(obj.packet_type, buffer, offset)

        return obj