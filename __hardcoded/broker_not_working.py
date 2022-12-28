from socketserver import StreamRequestHandler, ThreadingTCPServer


class TCPRequestHandler(StreamRequestHandler):
    def handle(self):        
        while True:
            data = self.rfile.readline().strip()
            request_str = f"[REQUEST] {self.client_address[0]}:{self.client_address[1]} <- ({data})\n"
            # if not data: break
            print(data)


if __name__ == '__main__':
    HOST, PORT = '127.0.0.1', 1883
    import socket
    HOST = socket.gethostbyname(socket.gethostname()) # 192.168.x.x
    tcp_server = ThreadingTCPServer((HOST, PORT), TCPRequestHandler)
    print(f"Server started at {HOST}:{PORT}")
    tcp_server.serve_forever()