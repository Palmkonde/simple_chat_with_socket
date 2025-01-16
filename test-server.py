import socket
import threading

HOST = '0.0.0.0'
PORT = 50005
server = None

clients = []


def broadcast(message: str, sender_socket: socket.socket) -> None:
    """ Sending messages from one to evey clients"""
    for client in clients:
        if client != sender_socket:
            client.send(message)


def send_message_function() -> None:
    """ Using for sending messages to client (server to clients) """
    while True:
        message = input("Enter a message: ")
        message = f"Server: {message}" + '\n'
        broadcast(message.encode(), None)


def handle_client(client_socket: socket.socket, client_address: str) -> None:
    """ Handle messages for each client """
    try:
        while True:
            message_received = ""

            # reciving a message
            while True:
                data = client_socket.recv(32)
                if data:
                    print('Received data chunk from client: ', repr(data))
                    message_received += data.decode()
                    if message_received.endswith("\n"):
                        break
                else:
                    # disconnected
                    print(f"{client_address} has disconnected")
                    raise ConnectionError

            if message_received:
                # show a message on server then send it to everyone
                print(f"Client {client_address}: ", message_received)

                message_with_address = f"Client {client_address}: {message_received}" + '\n'
                broadcast(message_with_address.encode(), client_socket)

    except ConnectionError:
        # Show on the server and send it to everyone
        print(f"Client {client_address} left the chat!")
        broadcast(
            f"Client {client_address} left the chat!\n".encode(), client_socket)

    finally:
        # clear and remove everything
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()


if __name__ == "__main__":
    # start initialize server socket
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
        print(f"Error binding/listening!: {msg}")
        server.close()
        exit(1)
    # end initial server socket

    # Thread for server to send messages
    send_thread = threading.Thread(target=send_message_function)
    send_thread.start()

    # main loop for handle client and others
    while True:
        client_socket, client_address = server.accept()
        print('Connection accepted from ', client_address)

        # add client to list
        clients.append(client_socket)

        # starting thread seperately
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address,))
        client_thread.start()
