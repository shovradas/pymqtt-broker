from middleware import Decoder

import socket

# HOST = '192.168.31.31'
HOST = '127.0.0.1'
PORT = 1883

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'\x10\x12\x00\x04MQTT\x05\x02\x00\x0b\x00\x00\x05ABCDE')    
    data = s.recv(1024)
    s.sendall(b'\x82\x1F\xff\xf6\x02\x0b\x01\x00\x0a\x73\x64\x2f\x74\x68\x69\x6e\x67\x2d\x31\x00\x00\x0a\x73\x64\x2f\x74\x68\x69\x6e\x67\x2d\x32\x00')
    s.sendall(b'\x82\x1F\xff\xf6\x02\x0b\x01\x00\x0a\x73\x64\x2f\x74\x68\x69\x6e\x67\x2d\x31\x00\x00\x0a\x73\x64\x2f\x74\x68\x69\x6e\x67\x2d\x32\x00')

print('Echo From Server: ', repr(data))

exit()
data = b'\x14\x11'
t = data[0] & 0b1111
# t = data[0]>>4
print(t, type(t))

data = b'\x001f78e0b19-7383-4a88-becc-0ff86a0f1e0e1650411877131\xc0\x00'
print(data[2:])


# def test_decoder_connect():
#     data = b'\x10\x11\x00\x04MQTT\x04\x02\x00\x0b\x00\x05abcde'
#     Decoder().connect(data)


# test_decoder_connect()


data = b'15'
print(type(data))