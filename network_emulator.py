import socket
import threading

class NetworkEmulator:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Network emulator listening on {self.host}:{self.port}")

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                # Process the data here or send it to another function
                print(f"Received data: {data}")
                client_socket.sendall(data)
        finally:
            client_socket.close()

    def run(self):
        try:
            while True:
                client_socket, addr = self.server.accept()
                print(f"Connection from {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except KeyboardInterrupt:
            print("\nShutting down the network emulator.")
        finally:
            self.server.close()

if __name__ == '__main__':
    emulator = NetworkEmulator()
    emulator.run()
