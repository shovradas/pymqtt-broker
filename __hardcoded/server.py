from socketserver import StreamRequestHandler, ThreadingTCPServer
import middleware

mw = middleware.Middleware()

class TCPRequestHandler(StreamRequestHandler):
    def handle(self):
        while True:
            data = self.rfile.readline() #.strip()
            print(f"[REQUEST] {self.client_address[0]}:{self.client_address[1]} <- ({data})")
            
            response = mw.handle_request(data)

            print(f"[RESPONSE] {self.client_address[0]}:{self.client_address[1]} -> ({response})")
            self.wfile.write(response)

            if (response[0]>>4) == 0xE: break


if __name__ == '__main__':
    HOST, PORT = '127.0.0.1', 1883
    # import socket
    # HOST = socket.gethostbyname(socket.gethostname()) # 192.168.x.x
    tcp_server = ThreadingTCPServer((HOST, PORT), TCPRequestHandler)
    tcp_server.serve_forever()