from common import PacketType


class ReasonCode:
    def __init__(self, packet_type, value, name, description=None) -> None:
        self.packet_type = packet_type
        self.value = value
        self.name = name
        self.description = description


class ReasonCodes:
    rules = {
        0:   {'Success': [PacketType.CONNACK, PacketType.PUBACK, PacketType.PUBREC, PacketType.PUBREL, PacketType.PUBCOMP, PacketType.UNSUBACK, PacketType.AUTH],
              'Normal disconnection': [PacketType.DISCONNECT],
              'Granted QoS 0': [PacketType.SUBACK]},
        1:   {'Granted QoS 1': [PacketType.SUBACK]},
        2:   {'Granted QoS 2': [PacketType.SUBACK]},
        4:   {'Disconnect with will message': [PacketType.DISCONNECT]},
        16:  {'No matching subscribers':  [PacketType.PUBACK, PacketType.PUBREC]},
        17:  {'No subscription found': [PacketType.UNSUBACK]},
        24:  {'Continue authentication': [PacketType.AUTH]},
        25:  {'Re-authenticate': [PacketType.AUTH]},
        128: {'Unspecified error': [PacketType.CONNACK, PacketType.PUBACK, PacketType.PUBREC, PacketType.SUBACK, PacketType.UNSUBACK, PacketType.DISCONNECT]},
        129: {'Malformed packet': [PacketType.CONNACK, PacketType.DISCONNECT]},
        130: {'Protocol error': [PacketType.CONNACK, PacketType.DISCONNECT]},
        131: {'Implementation specific error': [PacketType.CONNACK, PacketType.PUBACK, PacketType.PUBREC, PacketType.SUBACK, PacketType.UNSUBACK, PacketType.DISCONNECT]},
        132: {'Unsupported protocol version': [PacketType.CONNACK]},
        133: {'Client identifier not valid': [PacketType.CONNACK]},
        134: {'Bad user name or password': [PacketType.CONNACK]},
        135: {'Not authorized': [PacketType.CONNACK, PacketType.PUBACK, PacketType.PUBREC, PacketType.SUBACK, PacketType.UNSUBACK, PacketType.DISCONNECT], },
        136: {'Server unavailable': [PacketType.CONNACK]},
        137: {'Server busy': [PacketType.CONNACK, PacketType.DISCONNECT]},
        138: {'Banned': [PacketType.CONNACK]},
        139: {'Server shutting down': [PacketType.DISCONNECT]},
        140: {'Bad authentication method': [PacketType.CONNACK, PacketType.DISCONNECT]},
        141: {'Keep alive timeout': [PacketType.DISCONNECT]},
        142: {'Session taken over': [PacketType.DISCONNECT]},
        143: {'Topic filter invalid': [PacketType.SUBACK, PacketType.UNSUBACK, PacketType.DISCONNECT]},
        144: {'Topic name invalid': [PacketType.CONNACK, PacketType.PUBACK, PacketType.PUBREC, PacketType.DISCONNECT]},
        145: {'Packet identifier in use': [PacketType.PUBACK, PacketType.PUBREC, PacketType.SUBACK, PacketType.UNSUBACK]},
        146: {'Packet identifier not found': [PacketType.PUBREL, PacketType.PUBCOMP]},
        147: {'Receive maximum exceeded': [PacketType.DISCONNECT]},
        148: {'Topic alias invalid': [PacketType.DISCONNECT]},
        149: {'Packet too large': [PacketType.CONNACK, PacketType.DISCONNECT]},
        150: {'Message rate too high': [PacketType.DISCONNECT]},
        151: {'Quota exceeded': [PacketType.CONNACK, PacketType.PUBACK, PacketType.PUBREC, PacketType.SUBACK, PacketType.DISCONNECT], },
        152: {'Administrative action': [PacketType.DISCONNECT]},
        153: {'Payload format invalid': [PacketType.PUBACK, PacketType.PUBREC, PacketType.DISCONNECT]},
        154: {'Retain not supported': [PacketType.CONNACK, PacketType.DISCONNECT]},
        155: {'QoS not supported': [PacketType.CONNACK, PacketType.DISCONNECT]},
        156: {'Use another server': [PacketType.CONNACK, PacketType.DISCONNECT]},
        157: {'Server moved': [PacketType.CONNACK, PacketType.DISCONNECT]},
        158: {'Shared subscription not supported': [PacketType.SUBACK, PacketType.DISCONNECT]},
        159: {'Connection rate exceeded': [PacketType.CONNACK, PacketType.DISCONNECT]},
        160: {'Maximum connect time': [PacketType.DISCONNECT]},
        161: {'Subscription identifiers not supported': [PacketType.SUBACK, PacketType.DISCONNECT]},
        162: {'Wildcard subscription not supported': [PacketType.SUBACK, PacketType.DISCONNECT]},
    }

    def __init__(self, packet_type) -> None:
        self.packet_type = packet_type

    