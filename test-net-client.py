import socket
import threading

HOST = '10.237.28.221'
PORT = 21001

connecting_status = True

def send_message_function(client_socket):
    global connecting_status
    while True:
        message = input("Enter a message: ")
        client_socket.send((message + "\n").encode())
        
        if message.lower() == "exit":
            client_socket.close()
            connecting_status = False
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server")

    send_thread = threading.Thread(target=send_message_function, args=(s,))
    send_thread.start()

    while connecting_status:
        message_received = ""
        while True:
            data = s.recv(1024)
            if data:
                print('Received data chunk from server: ', repr(data))
                message_received += data.decode()
                if message_received.endswith("\n"):
                    print("End of message received")
                    break
            else:
                print("Connection lost!")
                connecting_status = False
                break
        if not message_received:
            break

        print("Server: ", message_received)

print("Client finished")