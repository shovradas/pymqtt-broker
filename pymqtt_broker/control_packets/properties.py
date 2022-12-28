from enum import Enum
from common import VariableByteInteger
from common import PacketType


class PropertyValueType(Enum):
    BYTE = 1
    TWO_BYTE_INTEGER = 2
    FOUR_BYTE_INTEGER = 3
    VARIABLE_BYTE_INTEGER = 4
    BINARY_DATA = 5
    UTF_8_ENCODED_STRING = 6
    UTF_8_STRING_PAIR = 7


class Properties:
    names = {
        'Payload Format Indicator':             1,  # 0x01
        'Message Expiry Interval':              2,  # 0x02
        'Content Type':                         3,  # 0x03
        'Response Topic':                       8,  # 0x08
        'Correlation Data':                     9,  # 0x09
        'Subscription Identifier':              11, # 0x0b
        'Session Expiry Interval':              17, # 0x11
        'Assigned Client Identifier':           18, # 0x12
        'Server Keep Alive':                    19, # 0x13
        'Authentication Method':                21, # 0x15
        'Authentication Data':                  22, # 0x16
        'Request Problem Information':          23, # 0x17
        'Will Delay Interval':                  24, # 0x18
        'Request Response Information':         25, # 0x19
        'Response Information':                 26, # 0x1a
        'Server Reference':                     28, # 0x1c
        'Reason String':                        31, # 0x1f
        'Receive Maximum':                      33, # 0x21
        'Topic Alias Maximum':                  34, # 0x22
        'Topic Alias':                          35, # 0x23
        'Maximum QoS':                          36, # 0x24
        'Retain Available':                     37, # 0x25
        'User Property':                        38, # 0x26
        'Maximum Packet Size':                  39, # 0x27
        'Wildcard Subscription Available':      40, # 0x28
        'Subscription Identifier Available':    41, # 0x29
        'Shared Subscription Available':        42  # 0x2a
    }
    rules = {
        1:  {'type': PropertyValueType.BYTE,                  'allow_multiple': False, 'allowed_packets': [PacketType.PUBLISH, PacketType.WILLMESSAGE]},
        2:  {'type': PropertyValueType.FOUR_BYTE_INTEGER,     'allow_multiple': False, 'allowed_packets': [PacketType.PUBLISH, PacketType.WILLMESSAGE]},
        3:  {'type': PropertyValueType.UTF_8_ENCODED_STRING,  'allow_multiple': False, 'allowed_packets': [PacketType.PUBLISH, PacketType.WILLMESSAGE]},
        8:  {'type': PropertyValueType.UTF_8_ENCODED_STRING,  'allow_multiple': False, 'allowed_packets': [PacketType.PUBLISH, PacketType.WILLMESSAGE]},
        9:  {'type': PropertyValueType.BINARY_DATA,           'allow_multiple': False, 'allowed_packets': [PacketType.PUBLISH, PacketType.WILLMESSAGE]},
        11: {'type': PropertyValueType.VARIABLE_BYTE_INTEGER, 'allow_multiple': False, 'allowed_packets': [PacketType.PUBLISH, PacketType.SUBSCRIBE]},
        17: {'type': PropertyValueType.FOUR_BYTE_INTEGER,     'allow_multiple': False, 'allowed_packets': [PacketType.CONNECT, PacketType.CONNACK, PacketType.DISCONNECT]},
        18: {'type': PropertyValueType.UTF_8_ENCODED_STRING,  'allow_multiple': False, 'allowed_packets': [PacketType.CONNACK]},
        19: {'type': PropertyValueType.TWO_BYTE_INTEGER,      'allow_multiple': False, 'allowed_packets': [PacketType.CONNACK]},
        21: {'type': PropertyValueType.UTF_8_ENCODED_STRING,  'allow_multiple': False, 'allowed_packets': [PacketType.CONNECT, PacketType.CONNACK, PacketType.AUTH]},
        22: {'type': PropertyValueType.BINARY_DATA,           'allow_multiple': False, 'allowed_packets': [PacketType.CONNECT, PacketType.CONNACK, PacketType.AUTH]},
        23: {'type': PropertyValueType.BYTE,                  'allow_multiple': False, 'allowed_packets': [PacketType.CONNECT]},
        24: {'type': PropertyValueType.FOUR_BYTE_INTEGER,     'allow_multiple': False, 'allowed_packets': [PacketType.WILLMESSAGE]},
        25: {'type': PropertyValueType.BYTE,                  'allow_multiple': False, 'allowed_packets': [PacketType.CONNECT]},
        26: {'type': PropertyValueType.UTF_8_ENCODED_STRING,  'allow_multiple': False, 'allowed_packets': [PacketType.CONNACK]},
        28: {'type': PropertyValueType.UTF_8_ENCODED_STRING,  'allow_multiple': False, 'allowed_packets': [PacketType.CONNACK, PacketType.DISCONNECT]},
        31: {'type': PropertyValueType.UTF_8_ENCODED_STRING,  'allow_multiple': False, 'allowed_packets': [PacketType.CONNACK, PacketType.PUBACK, PacketType.PUBREC, PacketType.PUBREL, PacketType.PUBCOMP, PacketType.SUBACK, PacketType.UNSUBACK, PacketType.DISCONNECT, PacketType.AUTH]},
        33: {'type': PropertyValueType.TWO_BYTE_INTEGER,      'allow_multiple': False, 'allowed_packets': [PacketType.CONNECT, PacketType.CONNACK]},
        34: {'type': PropertyValueType.TWO_BYTE_INTEGER,      'allow_multiple': False, 'allowed_packets': [PacketType.CONNECT, PacketType.CONNACK]},
        35: {'type': PropertyValueType.TWO_BYTE_INTEGER,      'allow_multiple': False, 'allowed_packets': [PacketType.PUBLISH]},
        36: {'type': PropertyValueType.BYTE,                  'allow_multiple': False, 'allowed_packets': [PacketType.CONNACK]},
        37: {'type': PropertyValueType.BYTE,                  'allow_multiple': False, 'allowed_packets': [PacketType.CONNACK]},
        38: {'type': PropertyValueType.UTF_8_STRING_PAIR,     'allow_multiple': True,  'allowed_packets': [PacketType.CONNECT, PacketType.CONNACK, PacketType.PUBLISH, PacketType.PUBACK, PacketType.PUBREC, PacketType.PUBREL, PacketType.PUBCOMP, PacketType.SUBSCRIBE, PacketType.SUBACK, PacketType.UNSUBSCRIBE, PacketType.UNSUBACK, PacketType.DISCONNECT, PacketType.AUTH, PacketType.WILLMESSAGE]},
        39: {'type': PropertyValueType.FOUR_BYTE_INTEGER,     'allow_multiple': False, 'allowed_packets': [PacketType.CONNECT, PacketType.CONNACK]},
        40: {'type': PropertyValueType.BYTE,                  'allow_multiple': False, 'allowed_packets': [PacketType.CONNACK]},
        41: {'type': PropertyValueType.BYTE,                  'allow_multiple': False, 'allowed_packets': [PacketType.CONNACK]},
        42: {'type': PropertyValueType.BYTE,                  'allow_multiple': False, 'allowed_packets': [PacketType.CONNACK]}
    }

    def __init__(self, packet_type) -> None:
        self.packet_type = packet_type

    def __setattr__(self, name, value) -> None:
        if not name in ['packet_type', 'property_length']:
            real_name = name.replace('_', ' ').title()
            if real_name not in Properties.names:
                raise Exception(f"No such property exists")
            else:
                identifier = Properties.names[real_name]
                rule = Properties.rules[identifier]
                if not self.packet_type in rule['allowed_packets']:
                    raise Exception(f"Property not allowed for {self.packet_type}")

                if rule['allow_multiple']:
                    if type(value) != type([]): value = [value]
                    if hasattr(self, name): value = getattr(self, name) + value

        super().__setattr__(name, value)

    def __encode_single(self, value, vtype):
        print(value)
        buffer = bytearray()
        if vtype == PropertyValueType.BYTE:
            buffer += value.to_bytes(1, 'big')
        elif vtype == PropertyValueType.TWO_BYTE_INTEGER:                    
            buffer += value.to_bytes(2, 'big')
        elif vtype == PropertyValueType.FOUR_BYTE_INTEGER:                    
            buffer += value.to_bytes(4, 'big')
        elif vtype == PropertyValueType.VARIABLE_BYTE_INTEGER:                    
            buffer += VariableByteInteger(value).bytes
        elif vtype == PropertyValueType.BINARY_DATA:
            buffer += value
        elif vtype == PropertyValueType.UTF_8_ENCODED_STRING:
            buffer += bytes(value, 'utf-8')
        elif vtype == PropertyValueType.UTF_8_STRING_PAIR:
            buffer += bytes(value[0], 'utf-8') + bytes(value[1], 'utf-8')
        print(buffer)

        return buffer

    def encode(self):
        buffer = bytearray()
        for real_name in Properties.names:
            name = real_name.lower().replace(' ', '_')
            if hasattr(self, name):
                value = getattr(self, name)
                
                # adding propery identifier
                identifier = self.names[real_name]
                buffer += VariableByteInteger(identifier).bytes

                rule = self.rules[identifier]
                vtype = rule['type']
                if rule['allow_multiple']:
                    for v in value:
                        buffer += self.__encode_single(v, vtype)
                else:
                    buffer += self.__encode_single(value, vtype)
        
        # adding property length
        buffer = VariableByteInteger(len(buffer)).bytes + buffer

        return buffer

    @classmethod
    def from_bytes(cls, packet_type, buffer, offset=0):
        properties = cls(packet_type)
        
        # reading property length
        properties.property_length = VariableByteInteger.from_bytes(buffer, offset)
        offset += properties.property_length.bytes_count

        end = offset + properties.property_length.value
        
        while offset < end:
            vbi = VariableByteInteger.from_bytes(buffer, offset)            
            identifier = vbi.value
            if identifier not in Properties.rules.keys():
                raise Exception(f"No such property exists")
            else:
                offset += vbi.bytes_count
                vtype = Properties.rules[identifier]['type']
                
                if vtype == PropertyValueType.BYTE:
                    value = int.from_bytes(buffer[offset], byteorder='big')
                    offset += 1
                elif vtype == PropertyValueType.TWO_BYTE_INTEGER:
                    value = int.from_bytes(buffer[offset:offset+2], byteorder='big')
                    offset += 2
                elif vtype == PropertyValueType.FOUR_BYTE_INTEGER:
                    value = int.from_bytes(buffer[offset:offset+4], byteorder='big')
                    offset += 4
                elif vtype == PropertyValueType.VARIABLE_BYTE_INTEGER:                    
                    vbi = VariableByteInteger.from_bytes(buffer, offset)
                    value = vbi.value
                    offset += vbi.bytes_count
                elif vtype == PropertyValueType.BINARY_DATA:
                    length = int.from_bytes(buffer[offset:offset+2], byteorder='big')
                    offset += 2
                    value = buffer[offset: offset+length]
                    offset += length
                elif vtype == PropertyValueType.UTF_8_ENCODED_STRING:
                    length = int.from_bytes(buffer[offset:offset+2], byteorder='big')
                    offset += 2
                    value = bytes(buffer[offset: offset+length], 'utf-8')
                    offset += length
                elif vtype == PropertyValueType.UTF_8_STRING_PAIR:
                    length = int.from_bytes(buffer[offset:offset+2], byteorder='big')
                    offset += 2
                    k = bytes(buffer[offset: offset+length], 'utf-8')
                    offset += length

                    length = int.from_bytes(buffer[offset:offset+2], byteorder='big')
                    offset += 2
                    v = bytes(buffer[offset: offset+length], 'utf-8')
                    offset += length
                    
                    value = (k, v)
                
                for item in Properties.names.items():
                    if item[1] == identifier:
                        name = item[0].lower().replace(' ', '_')
                        setattr(properties, name, value)
                        break
        
        return properties