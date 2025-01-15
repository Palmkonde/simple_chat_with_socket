import socket
import threading

HOST = '0.0.0.0'
PORT = 50005
server = None
client = []

def send_message_function(client_socket: socket.socket) -> None:
    """ Using for sending messages to client """
    while True:
        message = input("Enter a message: ")
        client_socket.send((message + "\n").encode())

def broad_cast(message: str,
               sender_socket: socket.socket) -> None:
    """ Sending messages from one to many clients"""
    pass

def handle_client(client_socket: socket.socket):
    """ Handle messages for each client """
    while True:
        data = client_socket.recv(1024)


# Start initialize server socket
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
except OSError as msg:
    server = None
    print(f"Error creating socket: {msg}")
    exit(1)

try:
    server.bind((HOST, PORT))
    server.listen()
    print(f"Socket bound and server is listening on {HOST}:{PORT}")
except OSError as msg:
    print("Error binding/listening!")
    server.close()
    exit(1)
# end initial server socket

# main loop for handle client and others
while True:
    client_socket, client_address = server.accept()
    with client_socket:
        print('Connection accepted from ', client_address)

        send_thread = threading.Thread(target=send_message_function, args=(client_socket, ))
        send_thread.start()

server.close()
print("Server finished")