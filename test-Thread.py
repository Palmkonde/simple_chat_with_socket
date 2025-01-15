import threading

def print_number():
    for i in range(10):
        print(i, end=" ")

def print_letters():
    for i in range(65, 75):
        print(chr(i), end=" ")

t1 = threading.Thread(target=print_number)
t2 = threading.Thread(target=print_letters)

t1.start()
t2.start()

t1.join()
t2.join()

print("Thread finish")