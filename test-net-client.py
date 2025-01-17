import socket
import threading

HOST = '127.0.0.1'
PORT = 50005

connecting_status = True

def send_message(server_socket: socket.socket) -> None:
    """ send a message to server """
    global connecting_status
    while True:
        message = input("Enter a message: ")
        server_socket.send((message + "\n").encode())
        
        if message.lower() == "!exit":
            server_socket.shutdown(socket.SHUT_RDWR) 
            server_socket.close()
            connecting_status = False
            break

if __name__ == "__main__":
    """ Open socket to connect the server """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print("Connected to server")

        # Thread for send a message
        send_thread = threading.Thread(target=send_message, args=(sock,))
        send_thread.start()

        try:
            # receiving messages
            while connecting_status:
                message_received = ""
                while True:
                    data = sock.recv(32)
                    if data:
                        print('received data chunk from server: ', repr(data))
                        message_received += data.decode()
                        if message_received.endswith("\n"):
                            break
                    else:
                        print("Connection lost!")
                        connecting_status = False
                        break
                print(message_received)

        except (ConnectionAbortedError, OSError):
            print("Socket Closed")
        
        finally:
            connecting_status = False
            print("Existing Client...")

    print("Client Closed")