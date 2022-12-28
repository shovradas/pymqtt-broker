from enum import Enum

class PacketType(Enum):
    CONNECT         = 1  # 0x1 # client2server
    CONNACK         = 2  # 0x2 # server2client
    PUBLISH         = 3  # 0x3 # client2server or server2client
    PUBACK          = 4  # 0x4 # client2server or server2client
    PUBREC          = 5  # 0x5 # client2server or server2client
    PUBREL          = 6  # 0x6 # client2server or server2client
    PUBCOMP         = 7  # 0x7 # client2server or server2client
    SUBSCRIBE       = 8  # 0x8 # client2server
    SUBACK          = 9  # 0x9 # server2client
    UNSUBSCRIBE     = 10 # 0xa # client2server
    UNSUBACK        = 11 # 0xb # server2client
    PINGREQ         = 12 # 0xc # client2server
    PINGRESP        = 13 # 0xd # server2client
    DISCONNECT      = 14 # 0xe # client2server or server2client
    AUTH            = 15 # 0xf # client2server or server2client
    WILLMESSAGE 	= 99 # 0x63 # special case


class VariableByteInteger:
    def __init__(self, value) -> None:
        self.value = value
        if not hasattr(self, 'bytes'):
            self.bytes = self.__encode()
            self.bytes_count = len(self.bytes)

    def __encode(self):
        number = self.value
        encoded_bytes = bytearray()

        number, encoded_byte = divmod(number, 128)
        if number > 0: encoded_byte |= 128
        encoded_bytes.append(encoded_byte)

        while number > 0:
            number, encoded_byte = divmod(number, 128)
            if number > 0: encoded_byte |= 128
            encoded_bytes.append(encoded_byte)
        
        return bytes(encoded_bytes)

    @classmethod
    def from_bytes(cls, buffer, offset=0):
        multiplier = 1
        value = 0

        i = offset or 0
        encoded_byte = buffer[i]
        value += (encoded_byte & 127) * multiplier
        if multiplier > 128*128*128: raise('Malformed Variable Byte Integer')
        multiplier *= 128
        
        while (encoded_byte & 128) != 0:
            i += 1
            encoded_byte = buffer[i]
            value += (encoded_byte & 127) * multiplier
            if multiplier > 128*128*128: raise('Malformed Variable Byte Integer')
            multiplier *= 128

        obj = cls(value)
        obj.bytes_count = i+1-offset
        obj.bytes = buffer[offset:i+1]
        
        return obj


if __name__ == '__main__':
    vbi = VariableByteInteger(16385)    
    print(vbi.__dict__)

    # print()
    
    vbi = VariableByteInteger.from_bytes(b'\x81\x80\x01')
    print(vbi.__dict__)

    print()

    vbi = VariableByteInteger.from_bytes(b'\x81\x80\x01\x02')
    print(vbi.__dict__)

    print()
    
    vbi = VariableByteInteger.from_bytes(b'\x10\x81\x80\x01\x02', 1)
    print(vbi.__dict__)