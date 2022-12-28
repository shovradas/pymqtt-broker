import json
import struct
from common import PacketType, VariableByteInteger

# Fixed Header ===============================================================
class ConnectFixedHeader:
    def __init__(self, packet_type, header_flags, remaining_length=None):
        self.packet_type = packet_type                       # 4 bits
        self.header_flags = header_flags                     # 4 bits
        self.remaining_length: VariableByteInteger = remaining_length             # variable byte(s)

    def encode(self):
        byte_0 = (self.packet_type.value << 4) | self.header_flags
        buffer = bytearray([byte_0])
        buffer += self.remaining_length.get_bytes()
        return buffer
# ============================================================================


# Variable Header ============================================================
class ConnectFlags:
    def __init__(self, clean_start=1, will_flag=0, will_qos=0, will_retain=0, password=0, user_name=0):
        self.clean_start = clean_start                                # 1 bit
        self.will_flag = will_flag                                    # 1 bit
        self.will_qos = will_qos                                      # 2 bits
        self.will_retain = will_retain                                # 1 bit
        self.password = password                                      # 1 bit
        self.user_name = user_name                                    # 1 bit

    @classmethod
    def from_int(cls, value: int):
        byte = format(value, '08b')

        user_name = int(byte[0])
        password = int(byte[1])
        will_retain = int(byte[2])
        will_qos = int(byte[3:5])
        will_flag = int(byte[5])
        clean_start = int(byte[6])

        return cls(clean_start, will_flag, will_qos, will_retain, password, user_name)

    def encode(self):        
        byte = f"{self.user_name}{self.password}{self.will_retain}{format(self.will_qos, '02b')}{self.will_flag}{self.clean_start}0"
        return int(byte, 2)

class ConnectProperties:
    def __init__(self):
        self.property_length = None
        self.session_expiry_interval = None
        self.receive_maximum = None
        self.maximum_packet_size = None
        self.topic_alias_maximum = None
        self.request_response_information = None
        self.request_problem_information = None
        self.user_property = None
        self.authentication_method = None
        self.authentication_data = None

class ConnectVariableHeader:
    def __init__(self, protocol_name, protocol_level, connect_flags, keep_alive, properties=None):
        self.protocol_name: str = protocol_name
        self.protocol_level: int = protocol_level
        self.connect_flags: ConnectFlags = connect_flags
        self.keep_alive: int = keep_alive
        self.connect_properties: ConnectProperties = properties

    def encode(self):
        buffer = bytearray()

        protocol_name = self.protocol_name.encode('utf-8')
        protocol_name_length = len(protocol_name)
        format = f"!H{protocol_name_length}sBBH"
        buffer += struct.pack(
            format,
            protocol_name_length,
            protocol_name,
            self.protocol_level,
            self.connect_flags.encode(),
            self.keep_alive
        )

        if self.connect_properties:
            pass # TODO: encode connect propertise
        else:
            buffer += b'\x00' # Setting absence of propertise
        
        return buffer
# ============================================================================


# Payload ====================================================================
class ConnectWillProperties:
    def __init__(self):
        self.property_length = None
        self.will_delay_interval = None
        self.payload_format_indicator = None
        self.message_expiry_interval = None
        self.content_type = None
        self.response_topic = None
        self.correlation_data = None
        self.user_property = None

class ConnectPayload:
    def __init__(self, client_id, will_properties=None, will_topic='', will_payload=None, user_name='', password=None):
        self.client_id: str = client_id
        self.will_properties: ConnectWillProperties = will_properties
        self.will_topic: str = will_topic
        self.will_payload = will_payload
        self.user_name: str = user_name
        self.password = password
# ============================================================================


class ConnectPacket:
    def __init__(self, fixed_header, variable_header, payload):
        self.fixed_header: ConnectFixedHeader = fixed_header
        self.variable_header: ConnectVariableHeader = variable_header
        self.payload: ConnectPayload = payload

    def __str__(self) -> str:
        return json.dumps(self, indent=2, default=lambda o: o.__dict__)

    def encode(self):
        buffer = bytearray()

        # PAYLOAD ============================================================
        client_id = self.payload.client_id.encode('utf-8')
        client_id_length = len(client_id)
        format = f"!H{client_id_length}s"
        buffer += struct.pack(format, client_id_length, client_id)

        if self.payload.will_properties:
            pass
            # TODO: set vh:connect flag
            # TODO: add to payload

        if self.payload.will_topic:
            pass
            # TODO: set vh:connect flag
            # TODO: add to payload

        if self.payload.will_payload:
            pass
            # TODO: set vh:connect flag
            # TODO: add to payload

        if self.payload.user_name:
            pass
            # TODO: set vh:connect flag
            # TODO: add to payload

        if self.payload.password:
            pass
            # TODO: set vh:connect flag
            # TODO: add to payload
                        

        # VARIABLE HEADER ====================================================
        buffer[0:0] = self.variable_header.encode()

        # FIXED HEADER =======================================================
        self.fixed_header.remaining_length = VariableByteInteger(len(buffer))
        buffer[0:0] = self.fixed_header.encode()

        return buffer

    @classmethod
    def from_bytes(cls, buffer: bytes):
        # DECODE FIXED HEADER ================================================
        offset = 0

        packet_type = PacketType(buffer[offset] >> 4)
        header_flags = buffer[offset] & 0x0F
        offset += 1

        remaining_length = VariableByteInteger.from_bytes(buffer, offset)
        offset += remaining_length.bytes_count

        fixed_header = ConnectFixedHeader(packet_type, header_flags, remaining_length)


        # DECODE VARIABLE HEADER =============================================
        protocol_name_length = int.from_bytes(buffer[offset:offset+2], byteorder='big') # TOCLARIFY: signed or unsigend?
        offset += 2

        protocol_name = buffer[offset: (offset + protocol_name_length)].decode('utf-8')
        offset += protocol_name_length

        protocol_level = buffer[offset]
        offset += 1

        connect_flags = ConnectFlags.from_int(buffer[offset])
        offset += 1

        keep_alive = int.from_bytes(buffer[offset: offset+2], 'big') # TOCLARIFY: signed or unsigend?
        offset += 2

        vbi = VariableByteInteger.from_bytes(buffer, offset)
        property_length = vbi.value
        offset += vbi.bytes_count

        properties = None
        if property_length:
            pass # TODO: parse properties

        variable_header = ConnectVariableHeader(protocol_name, protocol_level, connect_flags, keep_alive, properties)


        # DECODE PAYLOAD =====================================================
        client_id_length = int.from_bytes(buffer[offset: offset+2], 'big') # TOCLARIFY: signed or unsigend?
        offset += 2

        client_id = buffer[offset : (offset + client_id_length)].decode('utf-8')
        offset += client_id_length
        
        will_properties = None
        will_topic = None
        will_payload = None
        if variable_header.connect_flags.will_flag:
            pass # TODO: parse will_properties        
            pass # TODO: parse will_topic        
            pass # TODO: parse will_payload

        user_name = None
        if variable_header.connect_flags.user_name:
            pass # TODO: parse user_name

        password = None
        if variable_header.connect_flags.password:
            pass # TODO: parse user_name
 
        payload = ConnectPayload(client_id, will_properties, will_topic, will_payload, user_name, password)


        return cls(fixed_header, variable_header, payload)