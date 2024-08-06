import datetime
import socket
import threading
import time

IP_ADDR_SERVER = '172.20.10.3'
PORT_SERVER = 65325
NUM_CLIENTS = 1200
package_failure = 0
lock = threading.Lock()


def stress_test_client():
    global package_failure
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP_ADDR_SERVER, PORT_SERVER))
        for _ in range(5):
            client.sendall(b"connected")
        client.close()
    except socket.error as e:
        with lock:
            package_failure += 1
        print(f"Error: {e}")


def start_stress_test():
    threads = []
    for _ in range(NUM_CLIENTS):
        t = threading.Thread(target=stress_test_client)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


if __name__ == "__main__":
    start_time = time.time()
    start_stress_test()
    end_time = time.time()
    total_time = end_time - start_time
    print(f'Количество пакетов: {NUM_CLIENTS * 5}')
    print(f"Общее время выполнения: {total_time:.2f} секунд")
    print(f'Количество отказов {package_failure}')
