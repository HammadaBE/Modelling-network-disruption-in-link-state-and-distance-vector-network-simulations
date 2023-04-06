import socket

def send_data_to_emulator(host, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(data.encode())
        response = client_socket.recv(1024)
        print(f"Received response: {response.decode()}")

if __name__ == '__main__':
    emulator_host = '127.0.0.1'
    emulator_port = 12345
    data_to_send = "Hello, Network Emulator!"
    
    send_data_to_emulator(emulator_host, emulator_port, data_to_send)
