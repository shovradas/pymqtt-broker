from enum import Enum
import struct
from common import PacketType


class ConnectReasonCode:
    def __init__(self, value, name, description) -> None:
        self.value = value
        self.name = name
        self.description = description


CONNECT_REASON_CODES = {
    0: ConnectReasonCode(0, 'Success', 'The Connection is accepted.'),
    128: ConnectReasonCode(0, 'Unspecified error', 'The Server does not wish to reveal the reason for the failure, or none of the other Reason Codes apply.')
}


class ConnackVariableHeader:
    def __init__(self) -> None:
        self.connack_flags = 0
        self.connect_reason_code = 0
        self.properties = None


class ConnackPacket:
    def __init__(self, header_flags, remaining_length, connack_flags, reason_code):
        # Fixed Header
        self.packet_type = PacketType.CONNACK
        self.header_flags = header_flags
        self.remaining_length = remaining_length
        # Variable Header
        self.connack_flags = connack_flags
        self.reason_code = reason_code

    def encode(self):
        self.remaining_length = 3

        format = f"!BBBBB"
        packet = struct.pack(
            format,
            # header
            self.packet_type.value << 4,                    # control flag 0000
            self.remaining_length,
            # variable header
            self.connack_flags,
            self.reason_code,
            0
        )
        print(f"{format=}, {packet=}")
        return packet