from threading import Thread
from control_packets.simple_packets import SubscribeVariableHeader
from control_packets.properties import Properties
from common import PacketType
from control_packets.simple_packets import SubscribePacket


class Client:
    def connect(self): pass

    def publish(self): pass

    def subscribe(self, topic, options=None, properties=None, qos=0):
        variable_header = SubscribeVariableHeader(1, properties)
        SubscribePacket()

    def disconnect(self): pass