import socket
import threading
from client_interaction.auth import check_auth
from client_interaction.monitoring_system import screen_stream, monitoring_system
from client_interaction.network_scanning import make_scanning, list_ip_address
from client_interaction.system_info import give_system_info
from config import IP_ADDR_SERVER, PORT_SERVER
import logging


def up_server():
    while True:
        logging.info('% Ожидание пакета %')
        all_hosts = list_ip_address()
        client, address = server.accept()
        if address[0] not in all_hosts:
            logging.error(f'Хост с ip-адресом: {address[0]} не найден в списке хостов')
            client.close()
        else:
            logging.info(f'Пакет получен от {address[0]}')
            data = client.recv(1024)
            if 'screen' in data.decode():
                thread_screen = threading.Thread(target=screen_stream, args=(data, connected_clients))
                thread_screen.start()
            if data.decode() == 'connected':
                connected_clients[address] = client
                logging.info(f'К сокету подключился: {address[0]}')
            if 'auth' in data.decode():
                thread_auth = threading.Thread(target=check_auth, args=(client, data))
                thread_auth.start()
        # Пакет на сканирование сети
            if data.decode() == 'scan':
                thread_scan = threading.Thread(target=make_scanning)
                thread_scan.start()
            if data.decode() == 'give system info':
                thread_system_info = threading.Thread(target=give_system_info(connected_clients,))
                thread_system_info.start()
            if data.decode() == 'start monitoring':
                thread_start_monitoring = threading.Thread(target=monitoring_system(connected_clients,))
                thread_start_monitoring.start()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename="logging.log",
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt='%H:%M:%S',
    )
    connected_clients = {}
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP_ADDR_SERVER, PORT_SERVER))
    server.listen()
    up_server()


