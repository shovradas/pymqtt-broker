from struct import pack
from common import PacketType
from control_packets.connect_packet import ConnectPacket, ConnectFixedHeader, ConnectFlags, ConnectVariableHeader, ConnectPayload
from common import VariableByteInteger
from control_packets.simple_packets import PingRespPacket, PingReqPacket, DisconnectPacket, PublishPacket
from control_packets.simple_packets import SubscribePacket
from control_packets.properties import Properties
from control_packets.simple_packets import SubscribeAckPacket
from control_packets.simple_packets import UnsubAckPacket, UnsubscribePacket

def test_connect_flags():
    connect_flags = ConnectFlags(1, 0, 0, 0, 0, 0)
    print(connect_flags.encode())

    connect_flags.from_int(2)
    print(connect_flags.encode())

def test_connect_packet_decode():
    buffer = b'\x10\x12\x00\x04MQTT\x05\x02\x00\x0b\x00\x00\x05ABCDE'
    # buffer = b'\x10\x8a\x01\x00\x04MQTT\x04\x02\x00A\x00\x00}aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    packet = ConnectPacket.from_bytes(buffer)
    # print(packet.encode().hex('-'))
    print(packet.encode())

    assert packet.encode()==buffer

def test_connect_packet_encode():
    fh = ConnectFixedHeader(PacketType.CONNECT, 0)
    vh = ConnectVariableHeader('MQTT', 4, ConnectFlags(clean_start=1), 30, None)
    cp = ConnectPayload('A'*5)

    # print(fh.__dict__)
    # print(vh.__dict__)
    # print(cp.__dict__)
    packet = ConnectPacket(fh, vh, cp)
    # print(packet)
    print(packet.encode())
    print(packet.encode().hex('-'))

def test_connect_fixed_header():
    fh = ConnectFixedHeader(PacketType.CONNECT, 0, VariableByteInteger(138))
    print(fh.encode())

def test_connack_packet():
    pass

def test_pingreq_packet():
    packet = PingReqPacket()
    print(packet.encode())
    # assert packet.encode() == b'\xc0\x00'

    packet = PingReqPacket.from_bytes(b'\xc0\x00')
    print(packet.encode())


def test_pingresp_packet():
    packet = PingRespPacket()    
    print(packet.encode())
    # assert packet.encode() == b'\xd0\x00'

    packet = PingRespPacket.from_bytes(b'\xd0\x00')
    print(packet.encode())


def test_disconnect_packet():
    # packet = DisconnectPacket()    
    # print(packet.encode())    
    # assert packet.encode() == b'\xd0\x00'

    # packet = DisconnectPacket(DisconnectVariableHeader(0))
    # print(packet.encode())

    packet = DisconnectPacket.from_bytes(b'\xe0\x00')
    print(packet.__dict__)
    print(packet.encode())

    packet = DisconnectPacket.from_bytes(b'\xe0\x02\x00\x00')
    print(packet.__dict__)
    print(packet.encode())

    packet = DisconnectPacket.from_bytes(b'\xe0\x02\x01\x00')
    print(packet.__dict__)
    print(packet.encode())

def test_subscribe_packet():
    packet = SubscribePacket.from_bytes(b'\x82\x12\xff\xf6\x02\x0b\x01\x00\x0a\x73\x64\x2f\x74\x68\x69\x6e\x67\x2d\x31\x00')
    print(packet.__dict__)
    print(packet.encode().hex('-'))

    # Two topic filter
    packet = SubscribePacket.from_bytes(b'\x82\x1F\xff\xf6\x02\x0b\x01\x00\x0a\x73\x64\x2f\x74\x68\x69\x6e\x67\x2d\x31\x00\x00\x0a\x73\x64\x2f\x74\x68\x69\x6e\x67\x2d\x32\x00')
    print(packet.__dict__)
    print(packet.encode().hex('-'))

    # packet = SubscribePacket.from_bytes(b'\x82\x15\xff\xf6\x04\x0b\x01\x0b\x02\x00\rthings/thing1\x00')
    # print(packet.encode())
    

    # properties = Properties(PacketType.SUBSCRIBE)
    # properties.subscription_identifier = 1
    # properties.user_property=[("k1","v1"),("k2", "v2")]
    # properties.user_property=("k3","v3")

    # print(properties.__dict__)
    # print(properties.encode())

    # CONNACK Properties
    
    # p = Properties.from_bytes(PacketType.CONNACK, b'\x0b\x22\x00\x0a\x27\x00\x98\x96\x80\x21\x00\x14')
    # print(p.__dict__)

    # p = Properties(PacketType.CONNACK)
    # p.topic_alias_maximum = 10
    # p.maximum_packet_size = 10000000
    # p.receive_maximum = 20
    # print(p.__dict__)
    # print(p.encode().hex('-'))  # b'\x0b\x21\x00\x14\x22\x00\x0a\x27\x00\x98\x96\x80'

    # print(Properties.from_bytes(PacketType.CONNACK, p.encode()).__dict__)
    # print(properties.get_by_identifier(VariableByteInteger(11)))
    # print(*[x.__dict__ for x in properties.properties])
    # print(properties.encode().hex('-'))
    
    
    # variable_header = SubscribeVariableHeader(45454, )

    # print(Properties(PacketType.CONNACK).encode())

def test_suback_packet():
    packet = SubscribeAckPacket.from_bytes(b'\x90\x04\xff\xf6\x00\x00')
    print(packet.__dict__)
    print(packet.encode().hex('-'))

def test_unsubscribe_packet():
    packet = UnsubscribePacket.from_bytes(b'\xa2\x0f\xff\xf6\x00\x00\x0a\x73\x64\x2f\x74\x68\x69\x6e\x67\x2d\x31')
    print(packet.__dict__)
    print(packet.encode().hex('-'))

def test_unsuback_packet():
    packet = UnsubAckPacket.from_bytes(b'\xb0\x04\xff\xf6\x00\x00')
    print(packet.__dict__)
    print(packet.encode().hex('-'))

def test_publish_packet():
    packet = PublishPacket.from_bytes(b'\x30\x15\x00\x00\x10\x03\x00\x0a\x74\x65\x78\x74\x2f\x70\x6c\x61\x69\x6e\x23\x00\x02\x4f\x4e')
    print(packet.__dict__)
    print(packet.encode().hex('-'))

if __name__ == '__main__':
    # test_connect_packet_encode()
    # test_connect_packet_decode()
    # test_connect_flags()
    # test_connect_fixed_header()
    # test_connack_packet()    
    # test_pingreq_packet()
    # test_pingresp_packet()
    # test_disconnect_packet()
    # test_subscribe_packet()
    # test_suback_packet()

    # test_unsubscribe_packet()

    test_unsuback_packet()

    # packet = PingRespPacket.from_bytes(b'\xd0\x00')
    # print(packet, packet.__dict__)